# Deploy no Render.com (RECOMENDADO - Gratuito)

## Passo a Passo:

### 1. Criar conta no Render
- Acesse: https://render.com
- Clique em "Get Started for Free"
- Faça login com GitHub

### 2. Conectar repositório
- No dashboard do Render, clique em "New +"
- Selecione "Web Service"
- Conecte seu repositório GitHub: `cristiano-superacao/suameta`
- Clique em "Connect"

### 3. Configurar o serviço
```
Name: sistema-metas
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

### 4. Variáveis de ambiente
Adicione estas variáveis em "Environment":
```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura-aqui-123456789
DATABASE_URL=(será criado automaticamente ao adicionar PostgreSQL)
```

### 5. Adicionar banco de dados PostgreSQL
- No menu lateral, clique em "New +"
- Selecione "PostgreSQL"
- Name: `metas-db`
- Database: `metas`
- User: `metas_user`
- Region: Oregon (mesma do serviço)
- Plan: **Free**
- Clique em "Create Database"

### 6. Conectar banco ao serviço
- Volte ao Web Service
- Em "Environment", adicione:
  - Key: `DATABASE_URL`
  - Value: Cole a "Internal Database URL" do PostgreSQL criado

### 7. Deploy
- Clique em "Create Web Service"
- Aguarde o build (3-5 minutos)
- Acesse a URL fornecida: `https://sistema-metas.onrender.com`

---

# Deploy alternativo: Railway.app

## Passo a Passo:

### 1. Criar conta no Railway
- Acesse: https://railway.app
- Clique em "Login with GitHub"

### 2. Novo projeto
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Escolha: `cristiano-superacao/suameta`

### 3. Adicionar PostgreSQL
- Clique em "+ New"
- Selecione "Database" → "PostgreSQL"
- Será criado automaticamente

### 4. Configurar variáveis
Railway detecta automaticamente, mas confirme:
```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui
```

### 5. Deploy automático
- Railway faz deploy automaticamente
- URL: `https://suameta-production.up.railway.app`

---

# Características das plataformas:

## ✅ Render.com (RECOMENDADO)
- ✅ 750 horas/mês grátis
- ✅ PostgreSQL grátis (90 dias, depois expira)
- ✅ SSL automático
- ✅ Deploy automático do GitHub
- ✅ Logs completos
- ⚠️ Servidor hiberna após 15 min sem uso
- ⚠️ Primeiro acesso pode demorar 30s

## ✅ Railway.app
- ✅ $5 crédito grátis/mês
- ✅ PostgreSQL incluído
- ✅ SSL automático
- ✅ Mais rápido que Render
- ⚠️ Crédito limitado (pode acabar no fim do mês)

## ❌ Netlify (NÃO COMPATÍVEL)
- ❌ Apenas sites estáticos (HTML/CSS/JS)
- ❌ Não suporta Python/Flask
- ❌ Não suporta banco de dados

---

# Arquivos criados para deploy:

1. **Procfile** - Comando para iniciar o servidor
2. **runtime.txt** - Versão do Python
3. **requirements.txt** - Dependências (atualizado com gunicorn)
4. **render.yaml** - Configuração automática do Render
5. **.gitignore** - Ignora arquivos locais (.db, __pycache__, etc)

---

# Testar localmente antes do deploy:

```bash
# Instalar gunicorn
pip install gunicorn

# Testar servidor de produção
gunicorn app:app

# Acesse: http://127.0.0.1:8000
```

---

# Após o deploy:

1. Acesse a URL fornecida
2. Faça login: admin@metas.com / admin123
3. Cadastre vendedores, metas e equipes
4. Exporte relatórios em PDF
5. Compartilhe a URL com sua equipe!

🚀 **Bom deploy!**
