from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mysql.connector
import time

# Variáveis globais para o modelo
vectorizer = None
model = None

def treinar_modelo():
    """Treina o modelo de classificação com dados simulados."""
    global vectorizer, model
    
    # Exemplo de dados para treinamento (pode ser substituído por dados reais do banco)
    data = {
        "tarefa": [
            "Finalizar relatório do projeto", "Responder e-mails do trabalho", "Preparar apresentação para reunião", "Lançar notas que estao no Jira",
            "Estudar para a prova de cálculo", "Revisar matéria de programação", "Fazer exercícios de álgebra",
            "Organizar o armário", "Lavar roupa acumulada", "Limpar o banheiro"
        ],
        "classe": [
            "trabalho", "trabalho", "trabalho", "trabalho",
            "faculdade", "faculdade", "faculdade",
            "casa", "casa", "casa"
        ]
    }
    
    # Divisão em treino e teste
    X = data["tarefa"]
    y = data["classe"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Vetorização
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Treinamento
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)

    # Avaliação
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy:.2f}")

def sugerir_classe(tarefa):
    """Sugere uma classe com base no texto da tarefa."""
    global vectorizer, model
    if vectorizer is None or model is None:
        print("O modelo ainda não foi treinado!")
        return None
    
    tarefa_tfidf = vectorizer.transform([tarefa])
    classe = model.predict(tarefa_tfidf)[0]
    return classe

def adicionar_tarefa(tarefa):
    """Adiciona uma tarefa sugerindo automaticamente a classe."""
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='gestao_tarefas',
    )
    cursor = conexao.cursor()

    # Sugere a classe com base no texto
    classe_sugerida = sugerir_classe(tarefa)
    print(f"\nClasse sugerida para a tarefa: {classe_sugerida.capitalize()}\n")

    while True:
        classe = input(f"Escolha uma classe para essa tarefa (ou pressione Enter para aceitar '{classe_sugerida}'): ")
        if classe == "":
            classe = classe_sugerida
        if classe.lower() in ["trabalho", "faculdade", "casa"]:
            print("\n++++++++++++++++++++++++\nClasse adicionada\n++++++++++++++++++++++++\n")
            break
        else:
            print("Classe inválida. Escolha: Trabalho, Faculdade ou Casa.")

    # Converte para o tipo string padrão do Python
    tarefa = str(tarefa)
    classe = str(classe)

    # Adiciona ao banco de dados
    inserir = 'INSERT INTO tarefas_pendentes(tarefa, classe) VALUES (%s, %s)'
    cursor.execute(inserir, (tarefa, classe))
    conexao.commit()

    cursor.close()
    conexao.close()
if __name__ == "__main__":
    # Treina o modelo ao iniciar o programa
    print("Treinando o modelo de classificação...")
    treinar_modelo()

    while True:
        try:
            print("\n================================\n1-Adicionar uma tarefa.\n2-Excluir uma tarefa da lista.\n3-Listar tarefas\n4-Concluir uma tarefa\n5-Listar tarefas concluídas\n0-Finalizar o programa.\n================================\n")
            x = int(input("\nDigite a sua escolha:\n"))
        except:
            print("Erro na escolha, por favor coloque um valido")

        if x == 0:
            y = int(input("\nSeu programa será encerrado\nTem certeza?\n1-Sim\n2-Não\n"))
            if y == 1:
                print("\n---------Seu programa foi encerrado---------\n")
                break
            elif y == 2:
                continue
            else:
                print("\nDigite uma das opções\n")
        elif x == 1:
            tarefa = input("\nQual tarefa que você quer adicionar?\n")
            adicionar_tarefa(tarefa)
        elif x == 2:
            tarefa_remover = input("\nQual tarefa que você quer excluir?\n")
            excluir_tarefa(tarefa_remover)
        elif x == 3:
            print("\nAqui estão suas tarefas em ordem de prioridade\n")
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='gestao_tarefas',
            )
            cursor = conexao.cursor()
            consulta = 'SELECT tarefa, classe FROM tarefas_pendentes;'
            cursor.execute(consulta)
            listar_tarefas = cursor.fetchall()
            
            time.sleep(1)

            for linha in listar_tarefas:
                print(f"{linha}")
                time.sleep(0.5)
            cursor.close()
            conexao.close()
        elif x == 4:
            tarefa_concluida = input("\nDigite a tarefa a ser concluída:\n")
            concluirTarefa(tarefa_concluida)
        elif x == 5:
            print("Aqui está sua lista de tarefas concluídas...\n")
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='gestao_tarefas',
            )
            cursor = conexao.cursor()
            consulta = 'SELECT tarefa_concluida, classe_tarf FROM tarefas_concluidas;'
            cursor.execute(consulta)
            listar_tarefas = cursor.fetchall()
            for i in listar_tarefas:
                print(i)
            cursor.close()
            conexao.close()
        else:
            print("\nEscolha uma opção válida\n")