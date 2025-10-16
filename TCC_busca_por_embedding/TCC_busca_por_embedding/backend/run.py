#!/usr/bin/env python3
"""
Script para executar o servidor de busca semântica
"""

import os
import sys
from app import app, initialize_database

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Busca Semântica...")
    print("=" * 50)
    
    # Verificar se o banco de dados está configurado
    if not initialize_database():
        print("❌ Erro: Não foi possível inicializar o banco de dados")
        print("Verifique se o MariaDB está rodando e as configurações estão corretas")
        sys.exit(1)
    
    print("✅ Sistema inicializado com sucesso!")
    print("🌐 Servidor rodando em: http://localhost:5000")
    print("📊 Status: http://localhost:5000/health")
    print("🔍 Busca: http://localhost:5000/search")
    print("=" * 50)
    
    # Executar o servidor
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
