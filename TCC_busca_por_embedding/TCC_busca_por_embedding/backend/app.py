from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
from typing import List, Dict, Tuple
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'busca_semantica'),
    'charset': 'utf8mb4'
}

# Carregar o modelo de embedding
try:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    logger.info("Modelo de embedding carregado com sucesso")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    model = None

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = pymysql.connect(**self.config)
            logger.info("Conexão com banco de dados estabelecida")
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar com banco: {e}")
            return False
    
    def create_tables(self):
        """Cria as tabelas necessárias"""
        try:
            with self.connection.cursor() as cursor:
                # Tabela para armazenar perguntas e respostas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS questions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        embedding JSON,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabela para armazenar embeddings como vetores
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS question_embeddings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        question_id INT,
                        embedding_vector JSON,
                        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
                    )
                """)
                
                self.connection.commit()
                logger.info("Tabelas criadas com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            return False
    
    def insert_question(self, question: str, answer: str, embedding: List[float]) -> int:
        """Insere uma nova pergunta no banco"""
        try:
            with self.connection.cursor() as cursor:
                # Inserir pergunta
                cursor.execute("""
                    INSERT INTO questions (question, answer, embedding) 
                    VALUES (%s, %s, %s)
                """, (question, answer, json.dumps(embedding.tolist())))
                
                question_id = cursor.lastrowid
                
                # Inserir embedding
                cursor.execute("""
                    INSERT INTO question_embeddings (question_id, embedding_vector) 
                    VALUES (%s, %s)
                """, (question_id, json.dumps(embedding.tolist())))
                
                self.connection.commit()
                logger.info(f"Pergunta inserida com ID: {question_id}")
                return question_id
        except Exception as e:
            logger.error(f"Erro ao inserir pergunta: {e}")
            return None
    
    def get_all_questions(self) -> List[Dict]:
        """Recupera todas as perguntas do banco"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT q.id, q.question, q.answer, qe.embedding_vector
                    FROM questions q
                    LEFT JOIN question_embeddings qe ON q.id = qe.question_id
                """)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao recuperar perguntas: {e}")
            return []
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()

class SemanticSearch:
    def __init__(self, model, db_manager):
        self.model = model
        self.db_manager = db_manager
        self.questions_cache = []
        self.embeddings_cache = None
    
    def load_questions(self):
        """Carrega todas as perguntas do banco para cache"""
        self.questions_cache = self.db_manager.get_all_questions()
        if self.questions_cache:
            # Carregar embeddings do cache
            embeddings = []
            for q in self.questions_cache:
                if q['embedding_vector']:
                    embeddings.append(json.loads(q['embedding_vector']))
                else:
                    # Se não tem embedding, gerar um
                    embedding = self.model.encode([q['question']])[0]
                    embeddings.append(embedding.tolist())
                    # Atualizar no banco
                    self.db_manager.update_embedding(q['id'], embedding)
            
            self.embeddings_cache = np.array(embeddings)
            logger.info(f"Carregadas {len(self.questions_cache)} perguntas no cache")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Realiza busca semântica"""
        if not self.model:
            return []
        
        if not self.questions_cache:
            self.load_questions()
        
        if not self.questions_cache:
            return []
        
        # Gerar embedding da consulta
        query_embedding = self.model.encode([query])[0]
        
        # Calcular similaridade coseno
        similarities = np.dot(self.embeddings_cache, query_embedding) / (
            np.linalg.norm(self.embeddings_cache, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Obter top-k resultados
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold mínimo de similaridade
                results.append({
                    'question': self.questions_cache[idx]['question'],
                    'answer': self.questions_cache[idx]['answer'],
                    'similarity': float(similarities[idx])
                })
        
        return results

# Inicializar componentes
db_manager = DatabaseManager(DB_CONFIG)
semantic_search = SemanticSearch(model, db_manager)

@app.route('/search', methods=['POST'])
def search():
    """Endpoint para busca semântica"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Pergunta não fornecida'}), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({'error': 'Pergunta não pode estar vazia'}), 400
        
        # Realizar busca
        results = semantic_search.search(question)
        
        return jsonify({
            'results': results,
            'query': question,
            'total_results': len(results)
        })
    
    except Exception as e:
        logger.error(f"Erro na busca: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/questions', methods=['GET'])
def get_questions():
    """Endpoint para listar todas as perguntas"""
    try:
        questions = db_manager.get_all_questions()
        return jsonify({'questions': questions})
    except Exception as e:
        logger.error(f"Erro ao listar perguntas: {e}")
        return jsonify({'error': 'Erro ao recuperar perguntas'}), 500

@app.route('/questions', methods=['POST'])
def add_question():
    """Endpoint para adicionar nova pergunta"""
    try:
        data = request.get_json()
        if not data or 'question' not in data or 'answer' not in data:
            return jsonify({'error': 'Pergunta e resposta são obrigatórias'}), 400
        
        question = data['question'].strip()
        answer = data['answer'].strip()
        
        if not question or not answer:
            return jsonify({'error': 'Pergunta e resposta não podem estar vazias'}), 400
        
        if not model:
            return jsonify({'error': 'Modelo de embedding não disponível'}), 500
        
        # Gerar embedding
        embedding = model.encode([question])[0]
        
        # Inserir no banco
        question_id = db_manager.insert_question(question, answer, embedding)
        
        if question_id:
            # Atualizar cache
            semantic_search.load_questions()
            return jsonify({
                'message': 'Pergunta adicionada com sucesso',
                'question_id': question_id
            })
        else:
            return jsonify({'error': 'Erro ao adicionar pergunta'}), 500
    
    except Exception as e:
        logger.error(f"Erro ao adicionar pergunta: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'db_connected': db_manager.connection is not None
    })

def initialize_database():
    """Inicializa o banco de dados com dados de exemplo"""
    if not db_manager.connect():
        logger.error("Não foi possível conectar ao banco de dados")
        return False
    
    if not db_manager.create_tables():
        logger.error("Não foi possível criar as tabelas")
        return False
    
    # Verificar se já existem perguntas
    existing_questions = db_manager.get_all_questions()
    if not existing_questions:
        # Adicionar perguntas de exemplo
        sample_questions = [
            {
                "question": "Como funciona a inteligência artificial?",
                "answer": "A inteligência artificial (IA) é um campo da ciência da computação que visa criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana, como reconhecimento de padrões, aprendizado e tomada de decisões."
            },
            {
                "question": "O que é machine learning?",
                "answer": "Machine Learning (aprendizado de máquina) é um subcampo da IA que permite aos computadores aprender e melhorar automaticamente através da experiência, sem serem explicitamente programados para cada tarefa."
            },
            {
                "question": "Como funciona o processamento de linguagem natural?",
                "answer": "O processamento de linguagem natural (NLP) é uma área da IA que se concentra na interação entre computadores e linguagem humana, permitindo que máquinas entendam, interpretem e gerem texto em linguagem natural."
            },
            {
                "question": "O que são redes neurais?",
                "answer": "Redes neurais são sistemas computacionais inspirados no funcionamento do cérebro humano, compostos por camadas de neurônios artificiais interconectados que processam informações e aprendem padrões complexos."
            },
            {
                "question": "Como funciona a busca semântica?",
                "answer": "A busca semântica é uma técnica que utiliza algoritmos de IA para entender o significado e contexto das consultas, permitindo encontrar resultados relevantes mesmo quando as palavras exatas não coincidem."
            }
        ]
        
        logger.info("Adicionando perguntas de exemplo...")
        for q in sample_questions:
            if model:
                embedding = model.encode([q["question"]])[0]
                db_manager.insert_question(q["question"], q["answer"], embedding)
        
        logger.info("Perguntas de exemplo adicionadas com sucesso")
    
    # Carregar perguntas no cache
    semantic_search.load_questions()
    
    return True

if __name__ == '__main__':
    # Inicializar banco de dados
    if initialize_database():
        logger.info("Sistema inicializado com sucesso")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Falha na inicialização do sistema")
