#!/usr/bin/env python3
"""
Script de teste para a API de busca semântica
"""

import requests
import json
import time

# URL base da API
BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de saúde"""
    print("🔍 Testando endpoint de saúde...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Modelo carregado: {data['model_loaded']}")
            print(f"✅ Banco conectado: {data['db_connected']}")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_search(question):
    """Testa o endpoint de busca"""
    print(f"\n🔍 Testando busca: '{question}'")
    try:
        response = requests.post(
            f"{BASE_URL}/search",
            json={"question": question},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados {data['total_results']} resultados")
            
            for i, result in enumerate(data['results'], 1):
                print(f"\n{i}. Pergunta: {result['question']}")
                print(f"   Resposta: {result['answer'][:100]}...")
                print(f"   Similaridade: {result['similarity']:.2%}")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_add_question(question, answer):
    """Testa o endpoint de adicionar pergunta"""
    print(f"\n➕ Adicionando pergunta: '{question}'")
    try:
        response = requests.post(
            f"{BASE_URL}/questions",
            json={"question": question, "answer": answer},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pergunta adicionada com ID: {data['question_id']}")
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_list_questions():
    """Testa o endpoint de listar perguntas"""
    print("\n📋 Listando todas as perguntas...")
    try:
        response = requests.get(f"{BASE_URL}/questions")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total de perguntas: {len(data['questions'])}")
            
            for i, q in enumerate(data['questions'][:3], 1):  # Mostrar apenas as 3 primeiras
                print(f"\n{i}. ID: {q['id']}")
                print(f"   Pergunta: {q['question']}")
                print(f"   Resposta: {q['answer'][:100]}...")
            
            if len(data['questions']) > 3:
                print(f"\n... e mais {len(data['questions']) - 3} perguntas")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes da API de Busca Semântica")
    print("=" * 60)
    
    # Aguardar um pouco para o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(2)
    
    # Teste 1: Saúde do sistema
    if not test_health():
        print("\n❌ Falha no teste de saúde. Verifique se o servidor está rodando.")
        return
    
    # Teste 2: Listar perguntas existentes
    test_list_questions()
    
    # Teste 3: Busca semântica
    test_questions = [
        "Como funciona a inteligência artificial?",
        "O que é machine learning?",
        "Como funciona o deep learning?",
        "O que são redes neurais?",
        "Como funciona a busca semântica?"
    ]
    
    for question in test_questions:
        test_search(question)
        time.sleep(1)  # Pausa entre testes
    
    # Teste 4: Adicionar nova pergunta
    test_add_question(
        "O que é processamento de linguagem natural?",
        "Processamento de linguagem natural (NLP) é uma área da inteligência artificial que se concentra na interação entre computadores e linguagem humana."
    )
    
    # Teste 5: Buscar a pergunta recém-adicionada
    test_search("O que é NLP?")
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    main()
