def read_characters(lang):
    file = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\characters\\' + lang + '.txt'
    with open(file, encoding="utf-8") as f:
        characters = f.read().splitlines()
        f.close()
    return characters

def read_words_file(lang, category):
    file = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\categories\\' + lang + '\\' + category + '.txt'
    with open(file, encoding="utf-8") as f:
        dictionary = f.read().splitlines()
        f.close()
    return dictionary

def read_input_file(file):
    with open(file, encoding="utf-8") as f:
        dictionary = f.read().upper().splitlines()
        f.close()
    return dictionary