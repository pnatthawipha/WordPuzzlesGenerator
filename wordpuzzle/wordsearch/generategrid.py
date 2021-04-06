import random
from .grid import Grid
from .readdata import read_input_file, read_words_file, read_characters
from collections import defaultdict
import numpy as np

GRID_SIZE = ['15x15', '17x17', '20x20', '22x22', '25x25', '27x27', '30x30']
WORDS = [12, 15, 20, 25, 30, 34, 36]
DIRECTIONS = ['ver-down', 'hor-left', 'di', 'ver-up', 'hor-right']
DIAGONALS = ['di-left-down', 'di-right-down', 'di-left-up', 'di-right-up']

wordsloc = []
characters = []
selectedwords = []
english_words = []
lang_words = []
numofwords = 0

def generate_word_search(wsdictionary, selectfromlist):
    global numofwords
    row = int(wsdictionary['grid_size'].split("x")[0])
    col = int(wsdictionary['grid_size'].split("x")[1])
    
    numofwords = calculate_words_in_grid(row)
    
    matrix, wordslist = generate_grid(row, col, wsdictionary, selectfromlist)
    matrix.fill_in_blanks(characters)
    matrix.add_word_list(wordslist)
    selectedwords.clear()
    return matrix

def random_directions():
    direction = random.choice(DIRECTIONS)
    if direction == 'di':
        direction = random.choice(DIAGONALS)
    return direction

def remove_special_characters(wordslist):
    words_with_directions = defaultdict(list)
    for word in wordslist:
        if ' ' in word:
            word = word.replace(' ', '')
        elif '-' in word:
            word = word.replace('-','')
        elif "'" in word:
            word = word.replace("'", '')
        words_with_directions[word].append(random_directions())
    return words_with_directions

def check_direction(argument, matrix, row, col, word):
    switcher = {
        'hor-left': matrix.check_avail_hor_left,
        'hor-right': matrix.check_avail_hor_right,
        'ver-down': matrix.check_avail_ver_down,
        'ver-up': matrix.check_avail_ver_up,
        'di-left-down': matrix.check_avail_di_left_down,
        'di-left-up': matrix.check_avail_di_left_up,
        'di-right-down': matrix.check_avail_di_right_down,
        'di-right-up': matrix.check_avail_di_right_up
    }
    if 'di' in argument:
        return switcher[argument](row, col, word, True)
    else:
        return switcher[argument](row, col, word)

def generate_grid(row, col, wsdictionary, fromlist):
    global wordsloc, selectedwords, characters
    
    if fromlist:
        lang = wsdictionary['lang']
        cate = wsdictionary['category']
        read_words(lang, cate)
        characters = read_characters(lang)
        selectedwords = generate_words(row, col, lang)
    elif not fromlist:
        selectedwords = read_input_file(wsdictionary['file'])
        characters = read_characters('English')
        lang = 'English'
    
    fillgrid = False
    while not fillgrid:
        wordslist = random.sample(selectedwords, numofwords)
        temp = wordslist
        if lang != 'English':
            words = []
            for word in wordslist:
                words.append(word.split('  -  ')[0])
            wordslist = words
        
        matrix = Grid(row, col, wordslist)
        words_with_directions = defaultdict(list)
        words_with_directions = remove_special_characters(wordslist)
        wordsloc.clear()
        for word in words_with_directions:
            found = False
            notfoundcount = 0
            while not found:
                i, j, found = check_direction(words_with_directions[word][0], matrix, row, col, word)
                if found:
                    end_i, end_j = matrix.add_word(word, i, j, words_with_directions[word][0])
                    wordsloc.append((word,(i,j),(end_i,end_j)))
                    if len(wordsloc) == len(wordslist):
                        found = True
                else:
                    notfoundcount += 1
                    newdirection = random_directions()
                    if newdirection != words_with_directions[word][0]:
                        words_with_directions[word][0] = newdirection
                    if notfoundcount > len(wordslist):
                        break
            if len(wordsloc) == len(wordslist):
                fillgrid = True
                break
            if notfoundcount > len(wordslist):
                del matrix, words_with_directions, wordslist
                break
            
    return matrix, temp

def read_words(lang, cate):
    global english_words, lang_words
    
    if lang == 'English':
        english_words = read_words_file(lang, cate)
    else:
        english_words = read_words_file('English', cate)
        lang_words = read_words_file(lang, cate)

def generate_words(row, col, lang):
    global english_words, lang_words
    wordslist = []
    if lang == 'English':
        for word in english_words:
            if len(word) < row and len(word) < col:
                wordslist.append(word.upper())
    else:
        for word, eng_word in zip(lang_words, english_words):
            if len(word) < row and len(word) < col:
                wordslist.append(word.upper() + "  -  " + eng_word.upper())
    return wordslist

def calculate_words_in_grid(row):
    for index, size in enumerate(GRID_SIZE):
        if str(row) in size:
            return WORDS[index]
    # return row + int(row*0.2)

def get_words_loc():
    global wordsloc
    return wordsloc

""" wordsearch_dictionary = {
    'lang': 'English',
    'category': 'fruits',
    'grid_size': '15x15'
    }
for j in range(50):
    mat = generate_word_search(wordsearch_dictionary, True)
    mat.print_grid()
    print(j) """