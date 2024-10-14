def remover_palavra_do_arquivo(nome_arquivo, palavra):
  """Remove uma palavra específica de um arquivo de texto.

  Args:
    nome_arquivo: O nome do arquivo de texto.
    palavra: A palavra a ser removida.
  """

  try:
    with open(nome_arquivo, "r") as arquivo:
      conteudo = arquivo.read()

    # Verifica se a palavra está no conteúdo antes de fazer a substituição
    if palavra in conteudo:
      conteudo_modificado = conteudo.replace(palavra, "")  # Substitui a palavra

      # Atualiza o conteúdo do arquivo com a nova string
      with open(nome_arquivo, "w") as arquivo:
        arquivo.write(conteudo_modificado)

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