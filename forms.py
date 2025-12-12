# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from models import Usuario, Vendedor, Equipe
import re

class LoginForm(FlaskForm):
    """Formulário de login"""
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])

class RegistroForm(FlaskForm):
    """Formulário de registro de novo usuário"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('senha', message='As senhas não coincidem')
    ])
    cargo = SelectField('Cargo', choices=[
        ('usuario', 'Usuário'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrador')
    ], default='usuario')
    
    def validate_email(self, email):
        """Valida se o email já existe"""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está cadastrado.')

class VendedorForm(FlaskForm):
    """Formulário de cadastro de vendedor"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    telefone = StringField('Telefone', validators=[
        Optional(),
        Length(max=20)
    ])
    cpf = StringField('CPF', validators=[
        Optional(),
        Length(min=11, max=14, message='CPF inválido')
    ])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[Optional()])
    equipe_id = SelectField('Equipe', coerce=int, validators=[Optional()])
    
    def __init__(self, vendedor_id=None, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.vendedor_id = vendedor_id
    
    def validate_email(self, email):
        """Valida se o email já existe (ignora próprio registro em edição)"""
        vendedor = Vendedor.query.filter_by(email=email.data).first()
        if vendedor and (self.vendedor_id is None or vendedor.id != self.vendedor_id):
            raise ValidationError('Este email já está cadastrado.')
    
    def validate_cpf(self, cpf):
        """Valida formato do CPF (ignora próprio registro em edição)"""
        if cpf.data:
            # Remove caracteres não numéricos
            cpf_numeros = re.sub(r'\D', '', cpf.data)
            if len(cpf_numeros) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')
            
            # Verifica se já existe (ignora próprio registro)
            vendedor = Vendedor.query.filter_by(cpf=cpf.data).first()
            if vendedor and (self.vendedor_id is None or vendedor.id != self.vendedor_id):
                raise ValidationError('Este CPF já está cadastrado.')

class MetaForm(FlaskForm):
    """Formulário de cadastro/edição de meta"""
    vendedor_id = SelectField('Vendedor', coerce=int, validators=[
        DataRequired(message='Vendedor é obrigatório')
    ])
    mes = SelectField('Mês', coerce=int, choices=[
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
        (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
        (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ], validators=[DataRequired(message='Mês é obrigatório')])
    ano = IntegerField('Ano', validators=[
        DataRequired(message='Ano é obrigatório')
    ])
    valor_meta = FloatField('Valor da Meta (R$)', validators=[
        DataRequired(message='Valor da meta é obrigatório')
    ])
    receita_alcancada = FloatField('Receita Alcançada (R$)', validators=[
        Optional()
    ], default=0.0)
    status_comissao = SelectField('Status da Comissão', choices=[
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Pago', 'Pago')
    ], default='Pendente')
    observacoes = TextAreaField('Observações', validators=[Optional()])

class AtualizarReceitaForm(FlaskForm):
    """Formulário simplificado para atualizar receita"""
    receita_alcancada = FloatField('Receita Alcançada (R$)', validators=[
        DataRequired(message='Receita é obrigatória')
    ])
    observacoes = TextAreaField('Observações', validators=[Optional()])

class EquipeForm(FlaskForm):
    """Formulário de cadastro de equipe"""
    nome = StringField('Nome da Equipe', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[
        DataRequired(message='Supervisor é obrigatório')
    ])
    
    def __init__(self, equipe_id=None, *args, **kwargs):
        super(EquipeForm, self).__init__(*args, **kwargs)
        self.equipe_id = equipe_id
    
    def validate_nome(self, nome):
        """Valida se o nome da equipe já existe (ignora próprio registro em edição)"""
        equipe = Equipe.query.filter_by(nome=nome.data).first()
        if equipe and (self.equipe_id is None or equipe.id != self.equipe_id):
            raise ValidationError('Já existe uma equipe com este nome.')
