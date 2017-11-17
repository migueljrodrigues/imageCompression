def lzwCode(txt):

    #cria dicionario para single characters
    codes = dict([(chr(x), x) for x in range(256)])

    response = []
    dictSize = 256
    currString = ""

    for ch in txt:

        currString += ch

        if currString not in codes:
            #inserir string no dicionario com o numero respectivo
            codes[currString] = dictSize
            #inserir no array de resposta a ultima insercao
            response.append(codes[currString[:-1]])

            dictSize += 1
            currString = ch

    #mete o ultimo
    response.append(codes[currString])

    return response

def lzwDecode(compData):

    #dicionario invertido
    decodes = dict([(x, chr(x)) for x in range(256)])

    prox = 256
    decompText = ""
    prevString = ""

    for ch in compData:

        if ch not in decodes:
            #inserir string no dicionario com o numero respectivo
            decodes[ch] = prevString + prevString[0]

        decompText += decodes[ch]

        if len(prevString) != 0:
            #se ja houver alguma coisa, meter no dicionario a soma
            decodes[prox] = prevString + decodes[ch][0]
            prox +=1

        #limpar com novo(s) caracter(es)
        prevString = decodes[ch]

    return decompText
