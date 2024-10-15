import mysql.connector 

conexao = mysql.connector.connect (
    host = 'localhost',
    user= 'root', 
    password = '',
    database ='gestao_tarefas',

)

cursor = conexao.cursor()

tarefa_criada = "Estudos"
classe_criada = "Faculdade"
horario_criado = "103000"
comenado =f'INSERT INTO tarefas_pendentes(tarefa, classe, horario_cria) VALUES ("{tarefa_criada}", "{classe_criada}", "{horario_criado}")'

cursor.execute(comenado)
conexao.commit()

cursor.close()
conexao.close()