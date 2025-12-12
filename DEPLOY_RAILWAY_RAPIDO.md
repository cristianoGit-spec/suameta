# 🚀 Deploy no Railway - Guia Rápido (3 minutos)

## ✅ Pré-requisitos (JÁ TEMOS!)
- ✅ Código no GitHub: https://github.com/cristianoGit-spec/suameta
- ✅ Procfile configurado
- ✅ requirements.txt pronto
- ✅ Python 3.11 configurado

---

## 📋 Passo a Passo Simplificado

### 1️⃣ Acessar Railway
🔗 Abra: **https://railway.app/login**

**Login:**
- Email: `cristiano.s.santos@ba.estudante.senai.br`
- Senha: `18042016`

---

### 2️⃣ Criar Novo Projeto (1 clique)
- Clique no botão: **"New Project"**
- Selecione: **"Deploy from GitHub repo"**
- Escolha: **cristianoGit-spec/suameta**

---

### 3️⃣ Configurar Variáveis (copiar e colar)
Railway vai detectar Python automaticamente. Adicione as variáveis:

**Clique em "Variables" e adicione:**

```
FLASK_ENV=production
SECRET_KEY=metas-super-secreto-2024-railway-production
PORT=5000
```

---

### 4️⃣ Adicionar Banco PostgreSQL (1 clique)
- No mesmo projeto, clique: **"New"**
- Selecione: **"Database"**
- Escolha: **"PostgreSQL"**
- Railway vai criar e conectar automaticamente!

---

### 5️⃣ Conectar Banco ao App
- Volte ao serviço web
- Em "Variables", adicione:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

(Railway vai preencher automaticamente a URL do banco)

---

### 6️⃣ Deploy Automático! 🎉
- Railway vai fazer o deploy automaticamente
- Aguarde 2-3 minutos
- Clique em "Settings" → "Generate Domain"
- Sua URL estará disponível!

---

## 🌐 Depois do Deploy

Sua aplicação estará em:
**https://suameta-production.up.railway.app** (ou similar)

### 🔐 Acessar o sistema:
```
Admin:
Email: admin@metas.com
Senha: admin123

Supervisor:
Email: supervisor@metas.com
Senha: super123
```

---

## ⚡ Comandos Railway CLI (Opcional - para depois)

Se quiser automatizar no futuro:

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Linkar projeto
railway link

# Deploy
railway up
```

---

## 🆘 Problemas Comuns

**1. Erro de build?**
- Verifique se o Python 3.11 foi detectado
- Railway deve rodar: `pip install -r requirements.txt`

**2. App não inicia?**
- Verifique as variáveis de ambiente
- O Procfile já está configurado: `web: gunicorn app:app`

**3. Banco não conecta?**
- Verifique se a variável `DATABASE_URL` está correta
- Deve apontar para o PostgreSQL criado

---

## 📞 Suporte Railway
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

---

✅ **Tudo pronto para deploy em 3 minutos!**
