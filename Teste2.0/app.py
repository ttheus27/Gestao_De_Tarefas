import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os
import time
import pickle

# Carrega o modelo treinado ou treina um novo se não existir
MODEL_FILE = "tarefa_model.pkl"
if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
else:
    # Dados de treinamento (substitua com seus próprios dados)
    tarefas = [
        ("Trabalho", "Fazer relatório", "Alta"),
        ("Faculdade", "Estudar para prova", "Média"),
        ("Casa", "Lavar roupa", "Baixa"),
        ("Trabalho", "Reuniao com cliente", "Alta"),
        ("Faculdade", "Trabalho em grupo", "Média"),
        ("Casa", "Comprar comida", "Baixa"),
        ("Trabalho", "Escrever email", "Média"),
        ("Faculdade", "Fazer exercícios", "Alta"),
        ("Casa", "Limpar casa", "Baixa"),
    ]

    X = [f"{desc} {classe}" for classe, desc, _ in tarefas]
    y = [prioridade for _, _, prioridade in tarefas]

    # Pré-processamento de texto
    nltk.download('punkt')
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words("portuguese")  # Use o idioma correto
    stemmer = nltk.stem.RSLPStemmer()

    def preprocessar_texto(texto):
        tokens = nltk.word_tokenize(texto)
        tokens = [token.lower() for token in tokens if token.isalnum() and token not in stopwords]
        tokens = [stemmer.stem(token) for token in tokens]
        return " ".join(tokens)

    X = [preprocessar_texto(texto) for texto in X]

    # Criação de features
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Divisão dos dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinamento do modelo
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Avaliação do modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy:.2f}")

    # Salvar o modelo treinado
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

def adicionar_tarefa():
    classe = input("Digite a classe da tarefa (Trabalho, Faculdade, Casa): ")
    descricao = input("Digite a descrição da tarefa: ")

    # Pré-processamento da descrição
    descricao = preprocessar_texto(f"{descricao} {classe}")
    
    # Predição da prioridade
    features = vectorizer.transform([descricao])
    prioridade = model.predict(features)[0]

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("tarefas.txt", "a") as f:
        f.write(f"{classe}|{descricao}|{prioridade}|{timestamp}\n")

    print("Tarefa adicionada com sucesso!")

def visualizar_tarefas():
    with open("tarefas.txt", "r") as f:
        tarefas = f.readlines()

    print("## Tarefas Pendentes ##")
    for i, tarefa in enumerate(tarefas):
        classe, descricao, prioridade, timestamp = tarefa.strip().split("|")
        print(f"{i+1}. [{prioridade}] {classe}: {descricao} ({timestamp})")

def concluir_tarefa():
    visualizar_tarefas()
    numero_tarefa = int(input("Digite o número da tarefa a ser concluída: ")) - 1

    with open("tarefas.txt", "r") as f:
        tarefas = f.readlines()

    tarefa_concluida = tarefas[numero_tarefa]

    with open("concluidas.txt", "a") as f:
        f.write(tarefa_concluida)

    del tarefas[numero_tarefa]

    with open("tarefas.txt", "w") as f:
        f.writelines(tarefas)

    print("Tarefa concluída com sucesso!")

def visualizar_concluidas():
    with open("concluidas.txt", "r") as f:
        tarefas_concluidas = f.readlines()

    print("## Tarefas Concluídas ##")
    for tarefa in tarefas_concluidas:
        classe, descricao, prioridade, timestamp = tarefa.strip().split("|")
        print(f"[{prioridade}] {classe}: {descricao} ({timestamp})")

while True:
    print("\n## Sistema de Gerenciamento de Tarefas ##")
    print("1. Adicionar Tarefa")
    print("2. Visualizar Tarefas")
    print("3. Concluír Tarefa")
    print("4. Visualizar Concluídas")
    print("5. Sair")

    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        adicionar_tarefa()
    elif opcao == "2":
        visualizar_tarefas()
    elif opcao == "3":
        concluir_tarefa()
    elif opcao == "4":
        visualizar_concluidas()
    elif opcao == "5":
        break
    else:
        print("Opção inválida.")