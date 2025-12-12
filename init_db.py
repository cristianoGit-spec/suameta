#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de inicialização automática do banco de dados
Cria todas as tabelas e um usuário admin padrão
"""

from app import app, db
from models import Usuario
import os

def init_database():
    """Inicializa o banco de dados com tabelas e dados iniciais"""
    
    with app.app_context():
        print("🔧 Inicializando banco de dados...")
        
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se já existe usuário admin
        admin = Usuario.query.filter_by(email='admin@suameta.com').first()
        
        if not admin:
            print("👤 Criando usuário administrador padrão...")
            admin = Usuario(
                nome='Administrador',
                email='admin@suameta.com',
                cargo='admin',
                ativo=True
            )
            admin.set_senha('admin123')  # ALTERAR EM PRODUÇÃO!
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuário admin criado!")
            print("   📧 Email: admin@suameta.com")
            print("   🔑 Senha: admin123")
            print("   ⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        else:
            print("ℹ️  Usuário admin já existe")
        
        print("✅ Banco de dados pronto para uso!")
        
        # Mostrar informações do banco
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if 'postgresql' in db_uri:
            print("🗄️  Banco: PostgreSQL (Produção)")
        else:
            print("🗄️  Banco: SQLite (Desenvolvimento)")

if __name__ == '__main__':
    init_database()
