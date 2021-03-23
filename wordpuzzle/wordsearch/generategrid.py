import random
from .grid import Grid
from .readdata import read_words_file, read_characters
from collections import defaultdict

GRID_SIZE = ['12x12', '15x15', '17x17', '20x20', '22x22', '25x25', '27x27', '30x30']
DIRECTIONS = ['ver-down', 'hor-left', 'di', 'ver-up', 'hor-right']
DIAGONALS = ['di-left-down', 'di-right-down', 'di-left-up', 'di-right-up']

def generate_word_search(wsdictionary):
    row = int(wsdictionary['grid_size'].split("x")[0])
    col = int(wsdictionary['grid_size'].split("x")[1])
    print(wsdictionary['lang'], wsdictionary['category'])
    selectedwords = generate_words(row, col, wsdictionary['lang'], wsdictionary['category'])
    characters = read_characters(wsdictionary['lang'])
    numofwords = calculate_words_in_grid(row)
    listofwords = random.sample(selectedwords, k=numofwords)

    if wsdictionary['lang'] == 'English':
        matrix = generate_grid(row, col, listofwords, wsdictionary)
        matrix.fill_in_blanks(characters)
        matrix.add_word_list(listofwords)
        return matrix
    else:
        words = []
        for word in listofwords:
            words.append(word.split('  -  ')[0])
        matrix = generate_grid(row, col, words, wsdictionary)
        matrix.fill_in_blanks(characters)
        matrix.add_word_list(listofwords)
        return matrix

def random_directions():
    direction = random.choice(DIRECTIONS)
    if direction == 'di':
        direction = random.choice(DIAGONALS)
    return direction

def restart_grid(wsdictionary):
    generate_word_search(wsdictionary)
    
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

def generate_grid(row, col, wordslist, wsdictionary):
    matrix = Grid(row, col, wordslist)
    words_with_directions = defaultdict(list)
    words_with_directions = remove_special_characters(wordslist)
    
    for word in words_with_directions:
        found = False
        notfoundcount = 0
        while not found:
            i, j, found = check_direction(words_with_directions[word][0], matrix, row, col, word)
            if found:
                matrix.add_word(word, i, j, words_with_directions[word][0])
            else:
                notfoundcount += 1
                newdirection = random_directions()
                if newdirection != words_with_directions[word][0]:
                    words_with_directions[word][0] = newdirection
                elif notfoundcount >= len(wordslist):
                    restart_grid(wsdictionary)
                       
        
    return matrix

def generate_words(row, col, lang, category):
    english_words = read_words_file('English', category)
    selected_words = []
    if lang == "English":
        for word in english_words:
            if len(word) < row and len(word) < col:
                selected_words.append(word.upper())
    else:
        lang_words = read_words_file(lang, category)
        for word, eng_word in zip(lang_words, english_words):
            if len(word) < row and len(word) < col:
                selected_words.append(word.upper() + "  -  " + eng_word.upper())

    return selected_words

def calculate_words_in_grid(row):
    return row + int(row*0.2)
