# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """Modelo de usuário para autenticação"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(50), default='usuario')  # 'admin', 'supervisor', 'usuario'
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com vendedores (se for supervisor)
    vendedores = db.relationship('Vendedor', backref='supervisor_obj', lazy=True, foreign_keys='Vendedor.supervisor_id')
    
    def set_senha(self, senha):
        """Gera hash da senha"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

class Vendedor(db.Model):
    """Modelo de vendedor"""
    __tablename__ = 'vendedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(14), unique=True)
    
    # Relacionamento com supervisor
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    supervisor_nome = db.Column(db.String(100))  # Denormalizado para facilitar consultas
    
    # Relacionamento com equipe
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com metas
    metas = db.relationship('Meta', backref='vendedor', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Vendedor {self.nome}>'

class Meta(db.Model):
    """Modelo de meta mensal"""
    __tablename__ = 'metas'
    
    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'), nullable=False)
    
    # Período da meta
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)
    
    # Valores
    valor_meta = db.Column(db.Float, nullable=False)
    receita_alcancada = db.Column(db.Float, default=0.0)
    
    # Comissão calculada
    percentual_alcance = db.Column(db.Float, default=0.0)
    comissao_total = db.Column(db.Float, default=0.0)
    
    # Status
    status_comissao = db.Column(db.String(20), default='Pendente')  # 'Pendente', 'Aprovado', 'Pago'
    observacoes = db.Column(db.Text)
    
    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índice composto para garantir uma meta por vendedor por mês
    __table_args__ = (
        db.UniqueConstraint('vendedor_id', 'mes', 'ano', name='_vendedor_mes_ano_uc'),
    )
    
    def calcular_comissao(self):
        """Calcula o percentual de alcance e a comissão"""
        from calculo_comissao import calcular_percentual_alcance, calcular_comissao
        
        if self.valor_meta <= 0:
            self.percentual_alcance = 0.0
            self.comissao_total = 0.0
            return
        
        self.percentual_alcance = calcular_percentual_alcance(self.receita_alcancada, self.valor_meta)
        self.comissao_total = calcular_comissao(self.receita_alcancada, self.percentual_alcance)
    
    def __repr__(self):
        return f'<Meta {self.vendedor_id} - {self.mes}/{self.ano}>'

class Equipe(db.Model):
    """Modelo de equipe de vendedores"""
    __tablename__ = 'equipes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    
    # Relacionamento com supervisor
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    supervisor = db.relationship('Usuario', backref='equipes_supervisionadas')
    
    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com vendedores
    vendedores = db.relationship('Vendedor', backref='equipe_obj', lazy=True, foreign_keys='Vendedor.equipe_id')
    
    def __repr__(self):
        return f'<Equipe {self.nome}>'

class Configuracao(db.Model):
    """Modelo para configurações do sistema"""
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descricao = db.Column(db.String(255))
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Configuracao {self.chave}>'
