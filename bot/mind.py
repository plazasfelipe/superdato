from fuzzywuzzy import process

def search(myDict, lookup):
    for key, value in myDict.items():
        if lookup in key:
            return value

def speak(message, terms):
    match_tema = process.extract(message, terms, limit=1)

    tema_buscado = match_tema[0][0]

    return tema_buscado
