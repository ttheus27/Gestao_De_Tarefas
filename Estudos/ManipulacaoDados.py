
def contatador(nome):
    with open (nome,"r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().lower()
        palavras = conteudo.split()
        contagem_palavras = {}
        for palavra in palavras:
            if palavra in contagem_palavras:
                contagem_palavras[palavra] += 1
            else:
                contagem_palavras[palavra] = 1
    return contagem_palavras


nome = "palavra.txt"
contagem=contatador(nome)
    

for palavra, contagem in sorted(contagem.items()):
    print(f"{palavra}: {contagem}")
    

