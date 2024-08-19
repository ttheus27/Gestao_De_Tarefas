import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os
import time

# Carrega o modelo de classificação (se existir)
def carrega_modelo():
    if os.path.exists('modelo.pkl'):
        return pickle.load(open('modelo.pkl', 'rb'))
    else:
        return None

# Treina o modelo de classificação
def treina_modelo():
    # Lê dados de treinamento
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
    tarefas = [t.strip().split('|') for t in tarefas]
    textos = [t[0] for t in tarefas]
    categorias = [t[1] for t in tarefas]

    # Prepara os dados
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(textos)
    y = categorias

    # Divide os dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Treina o modelo
    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)

    # Avalia o modelo
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)
    print("Acurácia do modelo:", acuracia)

    # Salva o modelo treinado
    pickle.dump(modelo, open('modelo.pkl', 'wb'))

    return modelo

# Adiciona uma nova tarefa
def adiciona_tarefa(tarefa, categoria):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open('tarefas.txt', 'a', encoding='utf-8') as f:
        f.write(f"{tarefa}|{categoria}|{timestamp}\n")
    print("Tarefa adicionada com sucesso!")

# Lista todas as tarefas
def lista_tarefas():
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
    if tarefas:
        for tarefa in tarefas:
            tarefa = tarefa.strip().split('|')
            print(f"Tarefa: {tarefa[0]} - Categoria: {tarefa[1]} - Criada em: {tarefa[2]}")
    else:
        print("Nenhuma tarefa encontrada.")

# Remove uma tarefa
def remove_tarefa(tarefa):
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
    with open('tarefas.txt', 'w', encoding='utf-8') as f:
        for t in tarefas:
            if t.strip().split('|')[0] != tarefa:
                f.write(t)
    print("Tarefa removida com sucesso!")

# Categoriza uma tarefa
def categoriza_tarefa(tarefa):
    modelo = carrega_modelo()
    if modelo is None:
        modelo = treina_modelo()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([tarefa])
    categoria_predita = modelo.predict(X)[0]
    print(f"A tarefa '{tarefa}' provavelmente pertence à categoria: {categoria_predita}")

# Interface de usuário
while True:
    print("\nEscolha uma opção:")
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("3 - Remover tarefa")
    print("4 - Categorizar tarefa")
    print("5 - Sair")
    opcao = input("Opção: ")

    if opcao == '1':
        tarefa = input("Digite a tarefa: ")
        categoria = input("Digite a categoria: ")
        adiciona_tarefa(tarefa, categoria)
    elif opcao == '2':
        lista_tarefas()
    elif opcao == '3':
        tarefa = input("Digite a tarefa a ser removida: ")
        remove_tarefa(tarefa)
    elif opcao == '4':
        tarefa = input("Digite a tarefa a ser categorizada: ")
        categoriza_tarefa(tarefa)
    elif opcao == '5':
        break
    else:
        print("Opção inválida.")