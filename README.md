# 🎯 Sistema de Gestão de Metas e Comissões - VERSÃO COMPLETA

Sistema profissional e completo para gerenciamento de metas de vendas, cálculo automático de comissões e acompanhamento de desempenho, desenvolvido com Python/Flask, SQLAlchemy e Bootstrap 5.

## ✨ Funcionalidades Principais

### 🔐 Sistema de Autenticação
- ✅ Login e registro de usuários
- ✅ Controle de acesso por perfil (Admin, Supervisor, Usuário)
- ✅ Segurança com hash de senhas
- ✅ Sessões persistentes

### 👥 Gerenciamento de Vendedores
- ✅ Cadastro completo de vendedores (nome, email, telefone, CPF)
- ✅ Vinculação com supervisores
- ✅ Vinculação com equipes
- ✅ Ativação/desativação de vendedores
- ✅ Histórico de performance

### 🏢 Gerenciamento de Equipes
- ✅ Criação e gestão de equipes de vendas
- ✅ Atribuição de supervisor por equipe
- ✅ Visualização detalhada da performance da equipe
- ✅ Estatísticas consolidadas por equipe
- ✅ Acompanhamento de metas por equipe

### 📊 Gerenciamento de Metas
- ✅ Criação de metas mensais individualizadas
- ✅ Acompanhamento de receita alcançada
- ✅ Cálculo automático de comissões
- ✅ Status de pagamento (Pendente, Aprovado, Pago)
- ✅ Filtros por período (mês/ano)
- ✅ Observações e notas em cada meta

### 📈 Dashboard Interativo
- ✅ Visualização em tempo real das métricas da equipe
- ✅ Ranking de vendedores por desempenho
- ✅ Cards de estatísticas (Receita, Meta, Alcance, Comissões)
- ✅ Barras de progresso coloridas por faixa
- ✅ Interface responsiva para todos os dispositivos

### 💾 Banco de Dados
- ✅ SQLite para desenvolvimento local
- ✅ PostgreSQL pronto para produção (nuvem)
- ✅ Migrations automáticas
- ✅ Relacionamentos entre tabelas

## 🎨 Faixas de Comissão

O sistema calcula a comissão baseado no percentual de alcance da meta individual:

| Alcance da Meta | Taxa de Comissão | Cor na Interface |
|-----------------|------------------|------------------|
| Até 50%         | 1%               | 🔴 Vermelho      |
| 51% - 75%       | 2%               | 🟠 Laranja       |
| 76% - 100%      | 3%               | 🔵 Azul          |
| 101% - 125%     | 4%               | 🟢 Verde Claro   |
| Acima de 125%   | 5%               | 🟢 Verde Escuro  |

**Fórmula**: `Comissão = Receita Alcançada × Taxa da Faixa`

## 📂 Estrutura do Projeto

```
Metas/
│
├── app.py                     # [ANTIGA] Versão simples sem autenticação
├── app_novo.py                # [NOVA] Versão completa com banco de dados
├── models.py                  # Modelos do banco (Usuario, Vendedor, Meta)
├── forms.py                   # Formulários com validação
├── config.py                  # Configurações do app
├── calculo_comissao.py        # Lógica de cálculo de comissões
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação
│
├── templates/
│   ├── dashboard.html         # Dashboard principal
│   ├── login.html             # Página de login
│   ├── registro.html          # Página de registro
│   ├── vendedores/
│   │   ├── lista.html         # Lista de vendedores
│   │   └── form.html          # Formulário vendedor
│   └── metas/
│       ├── lista.html         # Lista de metas
│       └── form.html          # Formulário meta
│
└── static/                    # Arquivos estáticos (CSS, JS, imagens)
```

## 🚀 Como Executar - VERSÃO COMPLETA

### 1. Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### 2. Instalação

**Passo 1**: Instale as dependências:

```powershell
pip install -r requirements.txt
```

### 3. Inicializar o Banco de Dados

**Primeira vez rodando o sistema**:

```powershell
python app.py
```

O banco de dados será criado automaticamente na primeira execução.

### 4. Acessar o Sistema

Abra seu navegador e acesse: **<http://127.0.0.1:5001/login>**

### 5. Inicializar Dados de Exemplo (Opcional)

Para popular o banco com dados de exemplo (recomendado para teste):

```powershell
python init_data.py
```

Isso criará:
- 1 usuário administrador
- 2 supervisores
- 3 equipes
- 6 vendedores
- 6 metas do mês atual

### 6. Primeiro Acesso

**Após executar init_data.py**, use as credenciais:

**Admin**:
- Email: `admin@metas.com`
- Senha: `admin123`

**Supervisor 1**:
- Email: `joao.silva@metas.com`
- Senha: `supervisor123`

**Supervisor 2**:
- Email: `maria.santos@metas.com`
- Senha: `supervisor123`

**Ou crie sua própria conta**:
1. Clique em "Criar conta agora"
2. Preencha os dados
3. Faça login

## 📱 Usando o Sistema

### 1. Criar Equipes
- Acesse "Equipes" no menu
- Clique em "Nova Equipe"
- Preencha nome, descrição e selecione o supervisor
- Salve a equipe

### 2. Cadastrar Vendedores
1. Acesse **Vendedores** → **Novo Vendedor**
2. Preencha os dados do vendedor (nome, email, telefone, CPF)
3. Vincule a um supervisor (opcional)
4. Vincule a uma equipe (opcional)
5. Salve

### 3. Criar Metas
1. Acesse **Metas** → **Nova Meta**
2. Selecione o vendedor
3. Defina o mês e ano
4. Defina o valor da meta
5. Informe a receita alcançada (pode ser 0 inicialmente)
6. O sistema calcula automaticamente a comissão
7. Salve

### 4. Acompanhar Performance
- **Dashboard**: Veja o ranking geral e estatísticas consolidadas
- **Equipes**: Veja detalhes de cada equipe com performance dos vendedores
- **Metas**: Filtre por mês/ano para acompanhar resultados históricos

### 5. Atualizar Receita

1. Acesse **Metas** → **Lista de Metas**
2. Clique em **Editar** na meta desejada
3. Atualize o campo "Receita Alcançada"
4. O sistema recalcula automaticamente a comissão
5. Salve

### 4. Visualizar Dashboard

1. Acesse **Dashboard** (página inicial)
2. Veja as métricas gerais da equipe
3. Confira o ranking de vendedores
4. Filtre por mês/ano se necessário

## 🌐 Configurar Banco de Dados na Nuvem

### Opção 1: PostgreSQL (Recomendado para produção)

**Serviços gratuitos suportados**:
- Supabase (https://supabase.com)
- Render (https://render.com)
- Railway (https://railway.app)
- Neon (https://neon.tech)

**Configuração**:

1. Crie um banco PostgreSQL no serviço escolhido
2. Copie a URL de conexão (formato: `postgresql://user:pass@host:port/db`)
3. Configure a variável de ambiente:

```powershell
$env:DATABASE_URL="postgresql://usuario:senha@host:porta/database"
```

4. Execute o app:

```powershell
python app_novo.py
```

### Opção 2: SQLite (Desenvolvimento Local)

Por padrão, o sistema usa SQLite. O arquivo `metas.db` será criado automaticamente.

## 🔧 Personalização

### Modificar Faixas de Comissão

Edite o arquivo `calculo_comissao.py`:

```python
FAIXAS_COMISSAO = [
    {'alcance_max_perc': 50, 'taxa': 0.01},   # 1%
    {'alcance_max_perc': 75, 'taxa': 0.02},   # 2%
    {'alcance_max_perc': 100, 'taxa': 0.03},  # 3%
    {'alcance_max_perc': 125, 'taxa': 0.04},  # 4%
    {'alcance_max_perc': 1000, 'taxa': 0.05}  # 5%
]
```

### Alterar Porta do Servidor

No arquivo `app_novo.py`, linha final:

```python
app.run(debug=True, port=5001)  # Mude 5001 para a porta desejada
```

## 🛡️ Segurança

- ✅ Senhas criptografadas com Werkzeug
- ✅ Proteção CSRF em todos os formulários
- ✅ Sessões seguras com cookies HTTP-only
- ✅ Validação de dados no backend
- ✅ Prevenção contra SQL Injection (SQLAlchemy ORM)

## 🌟 Próximos Recursos (Roadmap)

- [ ] Exportação de relatórios em PDF
- [ ] Gráficos interativos com Chart.js
- [ ] Notificações por email
- [ ] API REST completa
- [ ] App mobile (Progressive Web App)
- [ ] Integração com sistemas de CRM

## 📊 API REST

### Endpoints Disponíveis

**GET** `/api/ranking?mes=12&ano=2025`

Retorna o ranking de vendedores em JSON.

Exemplo de resposta:
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "supervisor": "Ana Costa",
    "meta": 30000.00,
    "receita_alcancada": 35000.00,
    "percentual_alcance": 116.67,
    "comissao_total": 1400.00,
    "status_comissao": "Pendente"
  }
]
```

## 🛠️ Tecnologias Utilizadas

**Backend**:
- Python 3.13
- Flask 3.0
- Flask-SQLAlchemy (ORM)
- Flask-Login (Autenticação)
- Flask-WTF (Formulários e CSRF)
- Werkzeug (Segurança)

**Frontend**:
- HTML5 + CSS3
- Bootstrap 5.3
- Bootstrap Icons
- Google Fonts (Inter)
- JavaScript (Vanilla)

**Banco de Dados**:
- SQLite (desenvolvimento)
- PostgreSQL (produção)

## 📝 Exemplo de Cálculo

**Vendedor**: Maria Santos  
**Meta Individual**: R$ 30.000,00  
**Receita Alcançada**: R$ 38.000,00  

**Cálculo**:
1. Percentual de Alcance = (38.000 / 30.000) × 100 = **126,67%**
2. Faixa: Acima de 125% → Taxa = **5%**
3. Comissão = 38.000 × 0,05 = **R$ 1.900,00**

## 🤝 Suporte

Para dúvidas, sugestões ou problemas:
- Consulte esta documentação
- Verifique os logs do servidor
- Revise as mensagens de erro no navegador

## 📄 Licença

Este projeto foi desenvolvido para fins de gestão interna de metas e comissões.

---

**Desenvolvido com ❤️ usando Python/Flask e Bootstrap**
