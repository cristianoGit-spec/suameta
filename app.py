# app.py - Sistema Completo com Autenticação e Banco de Dados
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from models import db, Usuario, Vendedor, Meta, Equipe
from forms import LoginForm, RegistroForm, VendedorForm, MetaForm, EquipeForm
from pdf_generator import gerar_pdf_metas, gerar_pdf_dashboard
from datetime import datetime
from sqlalchemy import func
import os

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Carregar configurações
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Inicializar extensões
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário pelo ID"""
    return Usuario.query.get(int(user_id))

# ===== ROTAS DE AUTENTICAÇÃO =====

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_senha(form.senha.data):
            if not usuario.ativo:
                flash('Sua conta está inativa. Entre em contato com o administrador.', 'warning')
                return redirect(url_for('login'))
            
            login_user(usuario)
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            
            # Redirecionar para a página solicitada ou dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de novo usuário"""
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            cargo=form.cargo.data
        )
        usuario.set_senha(form.senha.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))


# ===== ROTA PRINCIPAL - DASHBOARD =====

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal com métricas e ranking"""
    # Obter o mês e ano atuais
    hoje = datetime.now()
    mes_atual = request.args.get('mes', hoje.month, type=int)
    ano_atual = request.args.get('ano', hoje.year, type=int)
    
    # Buscar todas as metas do período
    metas = Meta.query.filter_by(mes=mes_atual, ano=ano_atual).join(Vendedor).all()
    
    # Processar dados para o dashboard
    vendedores_data = []
    for meta in metas:
        vendedores_data.append({
            'id': meta.id,
            'nome': meta.vendedor.nome,
            'supervisor': meta.vendedor.supervisor_nome or 'Sem supervisor',
            'meta': meta.valor_meta,
            'receita_alcancada': meta.receita_alcancada,
            'percentual_alcance': meta.percentual_alcance,
            'percentual_alcance_formatado': f"{meta.percentual_alcance:.2f}%",
            'comissao_total': meta.comissao_total,
            'comissao_total_formatada': f"R$ {meta.comissao_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'status_comissao': meta.status_comissao
        })
    
    # Ordenar por percentual de alcance (ranking)
    vendedores_data.sort(key=lambda x: x['percentual_alcance'], reverse=True)
    
    # Calcular resumo global
    total_receita = sum(v['receita_alcancada'] for v in vendedores_data)
    total_meta = sum(v['meta'] for v in vendedores_data)
    total_comissao = sum(v['comissao_total'] for v in vendedores_data)
    
    resumo_global = {
        'total_vendedores': len(vendedores_data),
        'total_receita': total_receita,
        'total_receita_formatada': f"R$ {total_receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'total_meta': total_meta,
        'total_meta_formatada': f"R$ {total_meta:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'total_comissao_formatada': f"R$ {total_comissao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'alcance_equipe': (total_receita / total_meta * 100) if total_meta > 0 else 0,
        'mes': mes_atual,
        'ano': ano_atual
    }
    
    return render_template('dashboard.html', 
                         vendedores=vendedores_data, 
                         resumo_global=resumo_global)


# ===== ROTAS DE VENDEDORES =====

@app.route('/vendedores')
@login_required
def lista_vendedores():
    """Lista todos os vendedores"""
    vendedores = Vendedor.query.filter_by(ativo=True).all()
    return render_template('vendedores/lista.html', vendedores=vendedores)


@app.route('/vendedores/novo', methods=['GET', 'POST'])
@login_required
def novo_vendedor():
    """Cadastrar novo vendedor"""
    form = VendedorForm()
    
    # Preencher choices de supervisores
    supervisores = Usuario.query.filter_by(cargo='supervisor', ativo=True).all()
    form.supervisor_id.choices = [(0, 'Selecione um supervisor')] + [(s.id, s.nome) for s in supervisores]
    
    # Preencher choices de equipes
    equipes = Equipe.query.filter_by(ativa=True).all()
    form.equipe_id.choices = [(0, 'Selecione uma equipe')] + [(e.id, e.nome) for e in equipes]
    
    if form.validate_on_submit():
        supervisor = Usuario.query.get(form.supervisor_id.data) if form.supervisor_id.data else None
        
        vendedor = Vendedor(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            cpf=form.cpf.data,
            supervisor_id=form.supervisor_id.data if form.supervisor_id.data else None,
            supervisor_nome=supervisor.nome if supervisor else None,
            equipe_id=form.equipe_id.data if form.equipe_id.data else None
        )
        
        db.session.add(vendedor)
        db.session.commit()
        
        flash(f'Vendedor {vendedor.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('lista_vendedores'))
    
    return render_template('vendedores/form.html', form=form, titulo='Novo Vendedor')


@app.route('/vendedores/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_vendedor(id):
    """Editar vendedor existente"""
    vendedor = Vendedor.query.get_or_404(id)
    form = VendedorForm(vendedor_id=id, obj=vendedor)
    
    # Preencher choices de supervisores
    supervisores = Usuario.query.filter_by(cargo='supervisor', ativo=True).all()
    form.supervisor_id.choices = [(0, 'Selecione um supervisor')] + [(s.id, s.nome) for s in supervisores]
    
    # Preencher choices de equipes
    equipes = Equipe.query.filter_by(ativa=True).all()
    form.equipe_id.choices = [(0, 'Selecione uma equipe')] + [(e.id, e.nome) for e in equipes]
    
    if form.validate_on_submit():
        supervisor = Usuario.query.get(form.supervisor_id.data) if form.supervisor_id.data else None
        
        vendedor.nome = form.nome.data
        vendedor.email = form.email.data
        vendedor.telefone = form.telefone.data
        vendedor.cpf = form.cpf.data
        vendedor.supervisor_id = form.supervisor_id.data if form.supervisor_id.data else None
        vendedor.supervisor_nome = supervisor.nome if supervisor else None
        vendedor.equipe_id = form.equipe_id.data if form.equipe_id.data else None
        
        db.session.commit()
        flash(f'Vendedor {vendedor.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('lista_vendedores'))
    
    return render_template('vendedores/form.html', form=form, titulo='Editar Vendedor', vendedor=vendedor)


@app.route('/vendedores/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_vendedor(id):
    """Desativar vendedor"""
    vendedor = Vendedor.query.get_or_404(id)
    vendedor.ativo = False
    db.session.commit()
    flash(f'Vendedor {vendedor.nome} desativado com sucesso!', 'success')
    return redirect(url_for('lista_vendedores'))


# ===== ROTAS DE METAS =====

@app.route('/metas')
@login_required
def lista_metas():
    """Lista todas as metas"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    metas = Meta.query.filter_by(mes=mes, ano=ano).join(Vendedor).all()
    return render_template('metas/lista.html', metas=metas, mes=mes, ano=ano)


@app.route('/metas/nova', methods=['GET', 'POST'])
@login_required
def nova_meta():
    """Cadastrar nova meta"""
    form = MetaForm()
    
    # Preencher choices de vendedores
    vendedores = Vendedor.query.filter_by(ativo=True).all()
    form.vendedor_id.choices = [(v.id, v.nome) for v in vendedores]
    
    if form.validate_on_submit():
        # Verificar se já existe meta para este vendedor neste período
        meta_existente = Meta.query.filter_by(
            vendedor_id=form.vendedor_id.data,
            mes=form.mes.data,
            ano=form.ano.data
        ).first()
        
        if meta_existente:
            flash('Já existe uma meta para este vendedor neste período!', 'warning')
            return render_template('metas/form.html', form=form, titulo='Nova Meta')
        
        meta = Meta(
            vendedor_id=form.vendedor_id.data,
            mes=form.mes.data,
            ano=form.ano.data,
            valor_meta=form.valor_meta.data,
            receita_alcancada=form.receita_alcancada.data,
            status_comissao=form.status_comissao.data,
            observacoes=form.observacoes.data
        )
        
        # Calcular comissão
        meta.calcular_comissao()
        
        db.session.add(meta)
        db.session.commit()
        
        flash('Meta cadastrada com sucesso!', 'success')
        return redirect(url_for('lista_metas'))
    
    return render_template('metas/form.html', form=form, titulo='Nova Meta')


@app.route('/metas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_meta(id):
    """Editar meta existente"""
    meta = Meta.query.get_or_404(id)
    form = MetaForm(obj=meta)
    
    # Preencher choices de vendedores
    vendedores = Vendedor.query.filter_by(ativo=True).all()
    form.vendedor_id.choices = [(v.id, v.nome) for v in vendedores]
    
    if form.validate_on_submit():
        # Verificar se há outra meta para este vendedor neste período (exceto a atual)
        meta_existente = Meta.query.filter_by(
            vendedor_id=form.vendedor_id.data,
            mes=form.mes.data,
            ano=form.ano.data
        ).filter(Meta.id != id).first()
        
        if meta_existente:
            flash('Já existe outra meta para este vendedor neste período!', 'warning')
            return render_template('metas/form.html', form=form, meta=meta, titulo='Editar Meta')
        
        meta.vendedor_id = form.vendedor_id.data
        meta.mes = form.mes.data
        meta.ano = form.ano.data
        meta.valor_meta = form.valor_meta.data
        meta.receita_alcancada = form.receita_alcancada.data
        meta.status_comissao = form.status_comissao.data
        meta.observacoes = form.observacoes.data
        
        # Recalcular comissão
        meta.calcular_comissao()
        
        db.session.commit()
        flash('Meta atualizada com sucesso!', 'success')
        return redirect(url_for('lista_metas'))
    
    return render_template('metas/form.html', form=form, titulo='Editar Meta', meta=meta)


@app.route('/metas/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_meta(id):
    """Deletar meta"""
    meta = Meta.query.get_or_404(id)
    db.session.delete(meta)
    db.session.commit()
    flash('Meta deletada com sucesso!', 'success')
    return redirect(url_for('lista_metas'))


@app.route('/metas/exportar-pdf')
@login_required
def exportar_pdf_metas():
    """Exportar relatório de metas em PDF"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    metas = Meta.query.filter_by(mes=mes, ano=ano).join(Vendedor).all()
    
    pdf_buffer = gerar_pdf_metas(metas, mes, ano)
    
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    filename = f"Relatorio_Metas_{meses[mes-1]}_{ano}.pdf"
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )


@app.route('/dashboard/exportar-pdf')
@login_required
def exportar_pdf_dashboard():
    """Exportar relatório do dashboard em PDF"""
    # Calcular resumo global
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    metas_mes = Meta.query.filter_by(mes=mes_atual, ano=ano_atual).all()
    
    resumo = {
        'total_vendedores': Vendedor.query.filter_by(ativo=True).count(),
        'receita_total': sum(m.receita_alcancada for m in metas_mes),
        'meta_total': sum(m.valor_meta for m in metas_mes),
        'comissao_total': sum(m.comissao_total for m in metas_mes)
    }
    
    # Buscar top vendedores
    vendedores = []
    for meta in sorted(metas_mes, key=lambda m: m.receita_alcancada, reverse=True):
        vendedores.append({
            'nome': meta.vendedor.nome,
            'receita': meta.receita_alcancada,
            'meta': meta.valor_meta,
            'percentual': meta.percentual_alcance,
            'comissao': meta.comissao_total
        })
    
    pdf_buffer = gerar_pdf_dashboard(resumo, vendedores)
    
    filename = f"Dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )


# ===== API ROUTES =====

@app.route('/api/ranking')
def api_ranking():
    """API: Retorna ranking de vendedores"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    metas = Meta.query.filter_by(mes=mes, ano=ano).join(Vendedor).all()
    
    dados = []
    for meta in metas:
        dados.append({
            'id': meta.id,
            'nome': meta.vendedor.nome,
            'supervisor': meta.vendedor.supervisor_nome,
            'meta': meta.valor_meta,
            'receita_alcancada': meta.receita_alcancada,
            'percentual_alcance': meta.percentual_alcance,
            'comissao_total': meta.comissao_total,
            'status_comissao': meta.status_comissao
        })
    
    dados.sort(key=lambda x: x['percentual_alcance'], reverse=True)
    return jsonify(dados)


# ===== ROTAS DE EQUIPES =====

@app.route('/equipes')
@login_required
def lista_equipes():
    """Lista todas as equipes"""
    equipes = Equipe.query.filter_by(ativa=True).all()
    
    # Adiciona estatísticas de cada equipe
    equipes_data = []
    for equipe in equipes:
        vendedores_count = Vendedor.query.filter_by(equipe_id=equipe.id, ativo=True).count()
        equipes_data.append({
            'equipe': equipe,
            'vendedores_count': vendedores_count,
            'supervisor': Usuario.query.get(equipe.supervisor_id)
        })
    
    return render_template('equipes/lista.html', equipes=equipes_data)


@app.route('/equipes/nova', methods=['GET', 'POST'])
@login_required
def nova_equipe():
    """Cadastrar nova equipe"""
    form = EquipeForm()
    
    # Preencher choices de supervisores
    supervisores = Usuario.query.filter(Usuario.cargo.in_(['supervisor', 'admin']), Usuario.ativo == True).all()
    form.supervisor_id.choices = [(s.id, s.nome) for s in supervisores]
    
    if form.validate_on_submit():
        equipe = Equipe(
            nome=form.nome.data,
            descricao=form.descricao.data,
            supervisor_id=form.supervisor_id.data
        )
        
        db.session.add(equipe)
        db.session.commit()
        
        flash(f'Equipe {equipe.nome} cadastrada com sucesso!', 'success')
        return redirect(url_for('lista_equipes'))
    
    return render_template('equipes/form.html', form=form, titulo='Nova Equipe')


@app.route('/equipes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_equipe(id):
    """Editar equipe existente"""
    equipe = Equipe.query.get_or_404(id)
    form = EquipeForm(equipe_id=id, obj=equipe)
    
    # Preencher choices de supervisores
    supervisores = Usuario.query.filter(Usuario.cargo.in_(['supervisor', 'admin']), Usuario.ativo == True).all()
    form.supervisor_id.choices = [(s.id, s.nome) for s in supervisores]
    
    if form.validate_on_submit():
        equipe.nome = form.nome.data
        equipe.descricao = form.descricao.data
        equipe.supervisor_id = form.supervisor_id.data
        
        db.session.commit()
        flash(f'Equipe {equipe.nome} atualizada com sucesso!', 'success')
        return redirect(url_for('lista_equipes'))
    
    return render_template('equipes/form.html', form=form, equipe=equipe, titulo='Editar Equipe')


@app.route('/equipes/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_equipe(id):
    """Deletar equipe (soft delete)"""
    equipe = Equipe.query.get_or_404(id)
    equipe.ativa = False
    db.session.commit()
    
    flash(f'Equipe {equipe.nome} desativada com sucesso!', 'success')
    return redirect(url_for('lista_equipes'))


@app.route('/equipes/<int:id>/detalhes')
@login_required
def detalhes_equipe(id):
    """Ver detalhes da equipe com vendedores e metas"""
    equipe = Equipe.query.get_or_404(id)
    vendedores = Vendedor.query.filter_by(equipe_id=equipe.id, ativo=True).all()
    supervisor = Usuario.query.get(equipe.supervisor_id)
    
    # Buscar metas do mês atual para os vendedores da equipe
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    vendedores_data = []
    for vendedor in vendedores:
        meta = Meta.query.filter_by(
            vendedor_id=vendedor.id,
            mes=mes_atual,
            ano=ano_atual
        ).first()
        
        vendedores_data.append({
            'vendedor': vendedor,
            'meta': meta
        })
    
    return render_template('equipes/detalhes.html', 
                         equipe=equipe,
                         supervisor=supervisor,
                         vendedores=vendedores_data,
                         mes=mes_atual,
                         ano=ano_atual)


# ===== COMANDOS CLI =====

@app.cli.command()
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print('✅ Banco de dados criado com sucesso!')


@app.cli.command()
def create_admin():
    """Cria um usuário administrador"""
    admin = Usuario(
        nome='Administrador',
        email='admin@metas.com',
        cargo='admin'
    )
    admin.set_senha('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print('✅ Usuário administrador criado!')
    print('   Email: admin@metas.com')
    print('   Senha: admin123')


# Inicialização automática do banco de dados
with app.app_context():
    try:
        db.create_all()
        print("✅ Tabelas do banco de dados criadas/verificadas!")
        
        # Criar usuário admin se não existir
        from models import Usuario
        admin = Usuario.query.filter_by(email='admin@suameta.com').first()
        if not admin:
            admin = Usuario(
                nome='Administrador',
                email='admin@suameta.com',
                cargo='admin',
                ativo=True
            )
            admin.set_senha('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado: admin@suameta.com / admin123")
    except Exception as e:
        print(f"⚠️  Aviso na inicialização do BD: {e}")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 SISTEMA DE GESTÃO DE METAS E COMISSÕES - VERSÃO COMPLETA")
    print("="*70)
    print("\n✨ Novos Recursos:")
    print("   🔐 Sistema de autenticação (Login/Registro)")
    print("   💾 Banco de dados SQLite/PostgreSQL")
    print("   👥 Gerenciamento de vendedores")
    print("   📊 Gerenciamento de metas")
    print("   🎯 Cálculo automático de comissões")
    print("\n📊 Servidor iniciado com sucesso!")
    print("🌐 Acesse: http://127.0.0.1:5000/login")
    print("⌨️  Pressione CTRL+C para parar o servidor\n")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5001)
