def remover_palavra_do_arquivo(nome_arquivo, palavra):
  """Remove uma palavra específica de um arquivo de texto.

<<<<<<< HEAD
  Args:
    nome_arquivo: O nome do arquivo de texto.
    palavra: A palavra a ser removida.
  """
=======
# def contatador(nome):
#     with open (nome,"r", encoding="utf-8") as arquivo:
#         conteudo = arquivo.read().lower()
#         palavras = conteudo.split()
#         contagem_palavras = {}
#         for palavra in palavras:
#             if palavra in contagem_palavras:
#                 contagem_palavras[palavra] += 1
#             else:
#                 contagem_palavras[palavra] = 1
#     return contagem_palavras
>>>>>>> 1093cf04d26c69b32c6f850db1cfe7c938e2e46f

  try:
    with open(nome_arquivo, "r") as arquivo:
      conteudo = arquivo.read()

<<<<<<< HEAD
    # Verifica se a palavra está no conteúdo antes de fazer a substituição
    if palavra in conteudo:
      conteudo_modificado = conteudo.replace(palavra, "")  # Substitui a palavra

      # Atualiza o conteúdo do arquivo com a nova string
      with open(nome_arquivo, "w") as arquivo:
        arquivo.write(conteudo_modificado)
=======
# nome = "palavra.txt"
# contagem=contatador(nome)
    

# for palavra, contagem in sorted(contagem.items()):
#     print(f"{palavra}: {contagem}")



def excluir_tarefa(tarefa): 
    arquivo  = open ("Estudodos/palavra.txt")




excluir_tarefa("teste")
    
>>>>>>> 1093cf04d26c69b32c6f850db1cfe7c938e2e46f

      print(f"Palavra '{palavra}' removida do arquivo '{nome_arquivo}'.")
    else:
      print(f"Erro: A palavra '{palavra}' não foi encontrada no arquivo.")

  except FileNotFoundError:
    print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")

# Obter o nome do arquivo e a palavra do usuário
nome_arquivo = "Estudos/palavra.txt"
palavra = input("Digite a palavra a ser removida: ")

# Chamar a função para remover a palavra
remover_palavra_do_arquivo(nome_arquivo, palavra)