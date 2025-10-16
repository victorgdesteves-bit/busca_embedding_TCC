# 📋 Guia de Instalação - Sistema de Busca Semântica

## 🚀 Instalação Rápida

### 1. Pré-requisitos
- Python 3.8 ou superior
- MariaDB 10.3 ou superior
- Git (opcional)

### 2. Configurar MariaDB

Execute os seguintes comandos no terminal do MariaDB:

```sql
-- Conectar como root
mysql -u root -p

-- Criar banco de dados
CREATE DATABASE busca_semantica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário
CREATE USER 'busca_user'@'localhost' IDENTIFIED BY 'busca_password_123';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON busca_semantica.* TO 'busca_user'@'localhost';
FLUSH PRIVILEGES;
```

**OU** execute o script SQL fornecido:
```bash
mysql -u root -p < setup_database.sql
```

### 3. Instalar Dependências Python

```bash
# Navegar para a pasta backend
cd backend

# Instalar dependências
pip install -r requirements.txt
```

### 4. Executar o Sistema

```bash
# Executar o backend
python run.py
```

### 5. Acessar o Frontend

Abra o arquivo `frontend/index.html` no seu navegador ou use um servidor local:

```bash
# Opção 1: Abrir diretamente
# Clique duas vezes no arquivo frontend/index.html

# Opção 2: Servidor local (Python)
cd frontend
python -m http.server 8000
# Acesse: http://localhost:8000

# Opção 3: Servidor local (Node.js)
npx serve frontend
```

## 🔧 Configuração Avançada

### Alterar Configurações do Banco

Edite o arquivo `backend/app.py` na seção `DB_CONFIG`:

```python
DB_CONFIG = {
    'host': 'seu_host',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'seu_banco',
    'charset': 'utf8mb4'
}
```

### Adicionar Perguntas via API

```bash
# Exemplo usando curl
curl -X POST http://localhost:5000/questions \
  -H "Content-Type: application/json" \
  -d '{
    "question": "O que é deep learning?",
    "answer": "Deep learning é um subcampo do machine learning que usa redes neurais com múltiplas camadas."
  }'
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro: "Access denied for user"
- Verifique se o usuário e senha estão corretos
- Confirme se o usuário tem privilégios no banco

### Erro: "Can't connect to MySQL server"
- Verifique se o MariaDB está rodando
- Confirme se a porta 3306 está aberta

### Frontend não carrega
- Verifique se o backend está rodando na porta 5000
- Abra o console do navegador (F12) para ver erros

## 📊 Testando o Sistema

1. **Teste de Saúde**: http://localhost:5000/health
2. **Listar Perguntas**: http://localhost:5000/questions
3. **Busca**: Use a interface web ou API

## 🎯 Próximos Passos

1. Adicione suas próprias perguntas e respostas
2. Ajuste o threshold de similaridade conforme necessário
3. Implemente autenticação se necessário
4. Configure HTTPS para produção
