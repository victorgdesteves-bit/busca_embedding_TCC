# 🚀 Como Executar o Sistema de Busca Semântica

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

1. **Python 3.8 ou superior**
   - Baixe em: https://www.python.org/downloads/
   - ✅ Marque "Add Python to PATH" durante a instalação

2. **MariaDB ou MySQL**
   - Baixe em: https://mariadb.org/download/
   - Ou use MySQL: https://dev.mysql.com/downloads/

## 🔧 Passo a Passo

### 1️⃣ **Configurar o Banco de Dados**

**Opção A: Usando o script SQL (Recomendado)**
```bash
# Abra o terminal/prompt de comando
mysql -u root -p < setup_database.sql
```

**Opção B: Manualmente**
1. Abra o MariaDB/MySQL
2. Execute os comandos:
```sql
CREATE DATABASE busca_semantica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'busca_user'@'localhost' IDENTIFIED BY 'busca_password_123';
GRANT ALL PRIVILEGES ON busca_semantica.* TO 'busca_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2️⃣ **Instalar Dependências Python**

```bash
# Navegue para a pasta do projeto
cd TCC_busca_por_embedding

# Entre na pasta backend
cd backend

# Instale as dependências
pip install -r requirements.txt
```

**Se der erro de permissão no Windows:**
```bash
pip install --user -r requirements.txt
```

### 3️⃣ **Executar o Sistema**

**Opção A: Script Automático (Windows)**
- Duplo clique no arquivo `start.bat`

**Opção B: Manual**
```bash
# Na pasta backend
python run.py
```

**Opção C: Usando o app.py diretamente**
```bash
# Na pasta backend
python app.py
```

### 4️⃣ **Abrir o Frontend**

**Opção A: Direto no navegador**
- Abra o arquivo `frontend/index.html` no seu navegador

**Opção B: Servidor local**
```bash
# Na pasta frontend
python -m http.server 8000
# Acesse: http://localhost:8000
```

## 🎯 **Testando o Sistema**

### 1. **Verificar se está funcionando**
- Acesse: http://localhost:5000/health
- Deve retornar: `{"status": "healthy", "model_loaded": true, "db_connected": true}`

### 2. **Testar a busca**
- Abra o frontend
- Digite uma pergunta como: "Como funciona a inteligência artificial?"
- Clique em "Buscar"

### 3. **Usar o script de teste**
```bash
# Na pasta raiz do projeto
python test_api.py
```

## 🐛 **Solução de Problemas Comuns**

### ❌ **Erro: "ModuleNotFoundError"**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ **Erro: "Access denied for user"**
- Verifique se o MariaDB está rodando
- Confirme se criou o usuário 'busca_user'
- Teste a conexão:
```bash
mysql -u busca_user -p
# Senha: busca_password_123
```

### ❌ **Erro: "Can't connect to MySQL server"**
- Verifique se o MariaDB está rodando
- No Windows: Verifique se o serviço está ativo
- No Linux: `sudo systemctl start mariadb`

### ❌ **Frontend não carrega**
- Verifique se o backend está rodando na porta 5000
- Abra o console do navegador (F12) para ver erros
- Teste: http://localhost:5000/health

### ❌ **Modelo não carrega**
- Verifique sua conexão com a internet
- A primeira execução baixa o modelo (pode demorar)
- Verifique se há espaço em disco suficiente

## 📊 **Verificando se Funcionou**

1. **Backend rodando**: http://localhost:5000/health
2. **Listar perguntas**: http://localhost:5000/questions
3. **Frontend**: Abra `frontend/index.html`
4. **Teste de busca**: Digite "machine learning" e veja os resultados

## 🎉 **Pronto!**

Se tudo funcionou, você verá:
- ✅ Backend rodando na porta 5000
- ✅ Frontend com interface de busca
- ✅ Resultados de busca semântica
- ✅ Perguntas de exemplo sobre IA

## 📞 **Precisa de Ajuda?**

Se algo não funcionar:
1. Verifique se todos os pré-requisitos estão instalados
2. Confirme se o MariaDB está rodando
3. Verifique os logs de erro no terminal
4. Teste cada componente separadamente
