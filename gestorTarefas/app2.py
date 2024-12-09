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
    

def excluir_tarefa(tarefa_remover):
    #Conexacao com banco
    conexao = mysql.connector.connect (
        host = 'localhost',
        user= 'root', 
        password = '',
        database ='gestao_tarefas',
        )
    cursor = conexao.cursor()


    print("\nVoce esta quase la para delatar esse tarefa -->",tarefa_remover,"<--\n")
    verificar_tabela= f'SELECT tarefa FROM tarefas_pendentes;'
    cursor.execute(verificar_tabela)


    y = input(f"\nVoce quer realmente excluir essa tarefa?\n'{tarefa_remover}'\n1-Sim\n2-Não\n")
    while True:

        if y == 1:
            try:
                 # Limpa quaisquer resultados pendentes antes de executar a nova query
                while cursor.nextset():
                    cursor.fetchall()

                deletar = 'DELETE FROM tarefas_pendentes WHERE tarefa = %s'
                cursor.execute(deletar, (tarefa_remover,)) 
                conexao.commit()

                if cursor.rowcount > 0:
                    print("\n---Tarefa deletada da sua lista de afazeres---\n")
                else:
                    print("\n---Tarefa não encontrada na sua lista de afazeres---\n")

                time.sleep(1.5)
                break
            except Exception as e: 
                print(f"Erro: {e}")
                time.sleep(1)
                break

        else:
            print("\nVoltando para a tela inicial\n")

            time.sleep(1.5)

            break


    cursor.close()
    conexao.close()

def concluirTarefa(tarefaConcluida):
    conexao = mysql.connector.connect (
    host = 'localhost',
    user= 'root', 
    password = '',
    database ='gestao_tarefas',
    )
    cursor = conexao.cursor()

    
    try:
        # Seleciona a tarefa que esta no banco
        select_tarefa = f'SELECT * FROM tarefas_pendentes WHERE tarefa = "{tarefaConcluida}"'
        cursor.execute(select_tarefa)

        # Armazena a a linha em tarefa_selecionada
        tarefa_selecionada = cursor.fetchone()
        print(tarefa_selecionada)

        # Insere o valor na tabela de concluidos
        insert_query = 'INSERT INTO tarefas_concluidas (id_tarf, tarefa_concluida, classe_tarf) VALUES (%s, %s, %s)'
        cursor.execute(insert_query, tarefa_selecionada)
        # Retira da tabela de pendencias
        excluir_pendencia = f'DELETE FROM tarefas_pendentes WHERE tarefa = "{tarefaConcluida}"'
        cursor.execute(excluir_pendencia)
        conexao.commit()
        time.sleep(1)
        print("Tarefa concluida")
    except:
        print("Erro: resultado nao encontrado")
        cursor.fetchall()


    cursor.close()
    conexao.close()
if __name__ == "__main__":
    # Treina o modelo ao iniciar o programa
    print("Treinando o modelo de classificação...")
    treinar_modelo()

    while True:
        print("\n================================\n1-Adicionar uma tarefa.\n2-Excluir uma tarefa da lista.\n3-Listar tarefas\n4-Concluir uma tarefa\n5-Listar tarefas concluídas\n0-Finalizar o programa.\n================================\n")
        x = input("\nDigite a sua escolha:\n")
        if not x.isdigit():  
            print("Escolha inválida. Por favor, digite um número.")
            continue
    
        x = int(x) 

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
            try:
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='gestao_tarefas',
                )
                cursor = conexao.cursor()
            except Exception as e: 
                print(f"Error:{e}")
            
            try:
                consulta = '''
                    SELECT tarefa, classe
                    FROM tarefas_pendentes
                    ORDER BY
                        CASE
                            WHEN classe = 'trabalho' THEN 1
                            WHEN classe = 'faculdade' THEN 2
                            WHEN classe = 'casa' THEN 3
                        END
                    '''
                cursor.execute(consulta)
                listar_tarefas = cursor.fetchall()
            except Exception as e: 
                print(f"Error:{e}")
                
            time.sleep(1)

            for tarefa, classe in listar_tarefas:
                print(f"Tarefa: {tarefa} | Classe: {classe.capitalize()}")
                time.sleep(0.2)
            
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
            time.sleep(1)

            print("\nEscolha uma opção válida\n") 

            time.sleep(1)