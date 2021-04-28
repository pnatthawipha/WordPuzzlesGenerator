import os

def getCurrentPath():
    script_dir = os.path.dirname(__file__)
    dirs = script_dir.split('\\');
    return '/'.join(dirs[:len(dirs)-1])

def read_characters(lang):
    path = getCurrentPath()
    rel_path = "data/characters/" + lang + '.txt'
    abs_file_path = os.path.join(path, rel_path)
    with open(abs_file_path, encoding="utf-8") as f:
        characters = f.read().splitlines()
        f.close()
    return characters

def read_words_file(lang, category):
    path = getCurrentPath()
    rel_path = 'data/categories/' + lang + '/' + category + '.txt'
    abs_file_path = os.path.join(path, rel_path)
    with open(abs_file_path, encoding="utf-8") as f:
        dictionary = f.read().splitlines()
        f.close()
    return dictionary

def read_input_file(file):
    with open(file, encoding="utf-8") as f:
        dictionary = f.read().upper().splitlines()
        f.close()
    return dictionary

