# 🔍 Sistema de Busca Semântica

Um sistema completo de busca semântica que utiliza embeddings para encontrar respostas relevantes baseadas no significado das perguntas, não apenas nas palavras-chave.

## Funcionalidades

- **Frontend**: Interface web moderna e responsiva em HTML/CSS/JavaScript
- **Backend**: API REST em Python com Flask
- **Busca Semântica**: Utiliza sentence-transformers para gerar embeddings
- **Banco de Dados**: MariaDB para armazenar perguntas, respostas e embeddings
- **Similaridade**: Cálculo de similaridade coseno para encontrar as melhores correspondências

## Pré-requisitos

- Python 3.8+
- MariaDB 10.3+
- Navegador web moderno

## Instalação

### 1. Configure o MariaDB

Execute o script SQL fornecido:
```bash
mysql -u root -p < setup_database.sql
```

Ou execute manualmente:
```sql
CREATE DATABASE busca_semantica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'busca_user'@'localhost' IDENTIFIED BY 'busca_password_123';
GRANT ALL PRIVILEGES ON busca_semantica.* TO 'busca_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Instale as dependências Python

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente (opcional)

Copie o arquivo `env_example.txt` para `.env` e ajuste as configurações:
```bash
cp env_example.txt .env
```

### 4. Execute o backend

```bash
python run.py
```

O servidor estará rodando em `http://localhost:5000`

### 5. Abra o frontend

Abra o arquivo `frontend/index.html` em seu navegador ou use um servidor local:

```bash
# Usando Python
cd frontend
python -m http.server 8000

# Usando Node.js
npx serve frontend
```

## 📖 Como Usar

1. **Fazer uma pergunta**: Digite sua pergunta na caixa de busca
2. **Ver resultados**: O sistema retornará as perguntas mais similares com suas respostas
3. **Adicionar perguntas**: Use a API para adicionar novas perguntas e respostas

## 🔧 API Endpoints

### `POST /search`
Busca semântica por perguntas similares.

**Request:**
```json
{
  "question": "Como funciona a IA?"
}
```

**Response:**
```json
{
  "results": [
    {
      "question": "Como funciona a inteligência artificial?",
      "answer": "A IA é um campo da ciência da computação...",
      "similarity": 0.85
    }
  ],
  "query": "Como funciona a IA?",
  "total_results": 1
}
```

### `GET /questions`
Lista todas as perguntas cadastradas.

### `POST /questions`
Adiciona uma nova pergunta e resposta.

**Request:**
```json
{
  "question": "O que é deep learning?",
  "answer": "Deep learning é um subcampo do machine learning..."
}
```

### `GET /health`
Verifica o status do sistema.

## 🏗️ Arquitetura

```
TCC_busca_por_embedding/
├── frontend/
│   └── index.html          # Interface web
├── backend/
│   ├── app.py              # API Flask
│   ├── run.py              # Script de execução
│   ├── requirements.txt    # Dependências Python
│   └── env_example.txt     # Exemplo de configuração
├── setup_database.sql      # Script de configuração do banco
└── README.md              # Documentação
```

## 🧠 Como Funciona

1. **Embedding**: Cada pergunta é convertida em um vetor numérico usando sentence-transformers
2. **Armazenamento**: Os embeddings são armazenados no MariaDB junto com as perguntas e respostas
3. **Busca**: Quando uma nova pergunta é feita, ela é convertida em embedding
4. **Similaridade**: Calcula a similaridade coseno entre o embedding da consulta e todos os embeddings armazenados
5. **Ranking**: Retorna as perguntas mais similares ordenadas por relevância

## 🔧 Configuração Avançada

### Modelo de Embedding
O sistema usa o modelo `paraphrase-multilingual-MiniLM-L12-v2` por padrão. Para alterar:

```python
# Em backend/app.py
model = SentenceTransformer('seu-modelo-aqui')
```

### Threshold de Similaridade
Ajuste o threshold mínimo de similaridade:

```python
# Em backend/app.py, método search()
if similarities[idx] > 0.1:  # Altere este valor
```

### Número de Resultados
Configure quantos resultados retornar:

```python
# Em backend/app.py, método search()
results = semantic_search.search(question, top_k=5)  # Altere o top_k
```

## 🐛 Solução de Problemas

### Erro de Conexão com Banco
- Verifique se o MariaDB está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão manualmente

### Modelo não Carrega
- Verifique sua conexão com a internet (primeira execução baixa o modelo)
- Confirme se há espaço suficiente em disco
- Verifique os logs para erros específicos

### Frontend não Conecta
- Confirme se o backend está rodando na porta 5000
- Verifique se há erros de CORS
- Teste a API diretamente com curl ou Postman

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Fazer commit das mudanças
4. Abrir um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório ou entre em contato.
