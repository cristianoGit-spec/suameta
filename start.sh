#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando Sistema de Metas..."

# Verificar se existe banco de dados
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  Usando SQLite (desenvolvimento)"
    export DATABASE_URL="sqlite:///metas.db"
else
    echo "✅ Conectando ao PostgreSQL..."
fi

# Criar tabelas se não existirem
python -c "
from app import db, app
with app.app_context():
    db.create_all()
    print('✅ Banco de dados inicializado!')
"

# Iniciar aplicação com gunicorn
echo "🌐 Iniciando servidor web..."
exec gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120
