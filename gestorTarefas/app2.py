import nltk
import mysql.connector 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os
import time
import pickle


# Estrutura para o sistema
# Sera com base em escolha de numeros


def adicionar_tarefa(tarefa):
    conexao = mysql.connector.connect (
    host = 'localhost',
    user= 'root', 
    password = '',
    database ='gestao_tarefas',
    )

    cursor = conexao.cursor()

    print("\nA tarefa que sera adcionada sera -->",tarefa,"<--\n")
    while True:
        classe = input("\nEscolha uma classe para essa tarefa:\nTrabalho\nEstudos\nCasa\n\n")
        
        # Faz verificação e adciona a classe junto com a tarefa
        if classe.lower() == "trabalho" or classe.lower() == "estudos"  or classe.lower() == "casa": 
            time.sleep(2)
            print("\n++++++++++++++++++++++++\nClasse adicionada\n++++++++++++++++++++++++\n")
            break
        else:
            print("Nao existe essa classe")
    # Coloca a classe e a tarefa no .TXT
    tarefa_nova = tarefa
    classe_tarefa = classe

    inserir = f'INSERT INTO tarefas_pendentes(tarefa, classe) VALUES ("{tarefa_nova}", "{classe_tarefa}")'
    cursor.execute(inserir)
    conexao.commit()

    cursor.close()
    conexao.close()

    # try:
    #     with open("gestorTarefas/lista.txt","a") as lista:
    #         lista.write(f"{tarefa} | {classe}\n")
    # except:
    #     print("Erro ao abrir o arquivo .TXT")
    
    # print("\n-------Tarefa adicionada na sua lista-------\n")
    
    

def excluir_tarefa(tarefa_remover):
    print("\nVoce esta quase la para delatar esse tarefa -->",tarefa_remover,"<--\n")
    y = int(input(f"\nVoce quer realmente excluir essa tarefa?\n'{tarefa_remover}'\n1-Sim\n2-Não\n"))
    while True:
        
        if y == 1:
                #Le o arquivo para armazenar em tarefas
            try:   
                with open("gestorTarefas/lista.txt", "r") as arquivo:
                    tarefas = arquivo.readlines()
            except FileNotFoundError:
                print("Erro: O arquivo de texto nao foi encontrado")

            except Exception as e :
                print("Um erro inesperado aconteceu: {e}")

            tarefa_encontrada = False
            with open("gestorTarefas/lista.txt", "w") as arquivo:
                    # Verifica linha por linha para tirar a solicitada
                for tarefa in tarefas:
                    if tarefa.strip().split('|')[0] != tarefa_remover:
                        arquivo.write(tarefa)  # Se a tarefa não for a removida, escreve ela de volta no arquivo
                    else:
                        tarefa_encontrada = True  # Marca como encontrada

            time.sleep(2)
            if tarefa_encontrada:
                print(f"Tarefa '{tarefa_remover}' foi removida com sucesso")
            else: 
                print(f"Tarefa '{tarefa_remover}' nao foi encontrada na lista")
            
            break 
        else:
            print("\nVoltando para a tela inicial\n")
            break
    
def concluirTarefa(tarefaConcluida):
    lista = open("gestorTarefas/concluidos.txt","a")
    lista.write(f"{tarefaConcluida}")
    print("\n++++++++++Tarefa concluida++++++++++")


# Começo do cogigo
while True:
    print("\n================================\n1-Adicionar uma tarefa.\n2-Excluir uma tarefa da lista.\n3-Listar tarefas\n4-Concluir uma tarefa\n5-Listar tarefas conclidas\n0-Finalizar o programa.\n================================\n")
    x = int(input("\nDigite a sua escolha:\n"))

    if x == 0 : 
        y = int(input("\nSeu programa sera encerrado\nTem certeza?\n1-Sim\n2-Nao\n"))
        if y == 1:
            print("\n---------Seu programa foi encerrado---------\n")
            break
        elif y == 2:
            continue
        else:
            print("\nDigite uma das opções\n")
    elif x == 1:
        tarefa = input("\nQual tarefa que voce quer adicionar?\n")
        adicionar_tarefa(tarefa)
    elif x == 2:
        tarefa_remover = input("\nQual tarefa que voce quer excluir?\n")
        excluir_tarefa(tarefa_remover)
    elif x == 3:
        print("\nAqui estao sua tarefa em ordem de prioridade\n")

        time.sleep(1)

        conexao = mysql.connector.connect (
        host = 'localhost',
        user= 'root', 
        password = '',
        database ='gestao_tarefas',
        )
        
        cursor = conexao.cursor()

        consutar = 'SELECT * FROM tarefas_pendentes'
        cursor.execute(consutar)
        listar_tarefas = cursor.fetchall()

        time.sleep(1)

        for linha in listar_tarefas:
            print (f"{linha}\n")

        cursor.close()
        conexao.close()
        
    elif x == 4:
        tarefaConcluida = input("\nDigite a tarefa a ser concluida:\n")
        concluirTarefa(tarefaConcluida)

    elif x == 5:
        print("\nAqui esta sua lista de itens concluidos:\n")
        with open("gestorTarefas/concluidos.txt") as concluidos:
            listaConclidos = concluidos.read()
            print (listaConclidos)
    else:
        print("\nEscolha uma opção valida\n")
    


