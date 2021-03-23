def read_characters(lang):
    category_dir = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\characters\\'
    with open(category_dir + lang + ".txt", encoding="utf-8") as file:
        characters = file.read().splitlines()
        file.close()
    return characters

def read_words_file(lang, category):
    category_dir = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\categories\\'
    with open(category_dir + lang + '\\' + category + '.txt', encoding="utf-8") as file:
        dictionary = file.read().splitlines()
        file.close()
    return dictionary