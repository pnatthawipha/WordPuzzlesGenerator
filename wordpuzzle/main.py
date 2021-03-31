import random
from tkinter import font
import PySimpleGUI as sg
import networkx as nx

from wordladder.graph import WordLadder
from wordladder.twl import check
from wordsearch.generategrid import generate_word_search, get_words_loc
from wordsearch.grid import Grid

LANGUAGES = ['English', 'Irish', 'French', 'German', 'Spanish', 'Italian']
CATEGORIES = ['animals', 'careers', 'colours', 'countries', 'emotions', 'flowers', 'fruits', 'shapes', 'sports', 'vegetables']
GRID_SIZE = ['15x15', '17x17', '20x20', '22x22', '25x25', '27x27']
LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Master']
COLOURS = ['blue', 'yellow', 'light pink', 'orange', 'lime', 'cyan']

BOX_SIZE = 25
BOX_PAD = 2.5
FONT = 'Helvetica,14'

MAX_ROWS = MAX_COLS = 7


def create_grid(win3, grid, wordsearch_dictionary):
    sizes = wordsearch_dictionary['grid_size'].split('x')

    g = win3['-WSGRAPH-']
    for row in range(int(sizes[0])):
        for col in range(int(sizes[1])):
            g.draw_rectangle((col * BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_PAD),
                             (col * BOX_SIZE + BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             line_color='black')
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 15.5, row * BOX_SIZE + 15.5),
                       font=("Helvetica", 12))


def find_word(win3, grid, start_i, start_j, end_i, end_j, solution):
    g = win3['-WSGRAPH-']
    colour = random.choice(COLOURS)
    if solution:
        colour = 'gray'

    for row in range(start_i, end_i + 1):
        for col in range(start_j, end_j + 1):
            g.draw_rectangle((col * BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_PAD),
                             (col * BOX_SIZE + BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 15.5, row * BOX_SIZE + 15.5),
                       font=("Helvetica", 12))

def find_word_di(win3, grid, start_i, start_j, word, solution):
    word = list(word)
    g = win3['-WSGRAPH-']
    colour = random.choice(COLOURS)
    if solution:
        colour = 'gray'
        
    i, j, found = grid.check_avail_di_left_down(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Helvetica", 12))
            i += 1
            j += 1
            found = False
        
    i, j, found = grid.check_avail_di_left_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Helvetica", 12))
            i -= 1
            j += 1
            found = False
                
    i, j, found = grid.check_avail_di_right_down(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Helvetica", 12))
            i += 1
            j -= 1
            found = False
            
    i, j, found = grid.check_avail_di_right_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Helvetica", 12))
            i -= 1
            j -= 1
            found = False
            
def get_word_search_gen_layout():
    layout = [[sg.Text('Select Language', font=FONT)],
              [sg.Combo(LANGUAGES, auto_size_text=True, default_value=LANGUAGES[0], enable_events=True, key='-WSLANGUAGE-', font=FONT)],
              [sg.Text('Select Category')],
              [sg.Combo(CATEGORIES, auto_size_text=True, default_value=CATEGORIES[0], enable_events=True, key='-WSCATEGORY-', font=FONT)],
              [sg.Text('Enter Grid Size')],
              [sg.Combo(GRID_SIZE, auto_size_text=True, default_value=GRID_SIZE[0], enable_events=True, key='-WSGRIDSIZE-', font=FONT)],
              [sg.Button('SUBMIT', font=FONT)],
              [sg.Button('BACK', font=FONT)]]
    return layout

def get_word_search_layout(row, col, wordslist):
    words = '\n'.join(wordslist)
    layout = [[sg.Graph((BOX_SIZE * row + 10, BOX_SIZE * col + 10), (0, BOX_SIZE * row + 10), (BOX_SIZE * col + 10, 0), background_color='white', key='-WSGRAPH-', enable_events=True, drag_submits=True),
               sg.VerticalSeparator(),
               sg.Text(words, key='-WSLIST-', font=FONT, text_color='Black')],
               [sg.Button('SOLUTION', font=FONT), sg.Button('HELP', font=FONT), sg.Button('NEXT', font=FONT), sg.Button('EXIT', font=FONT)]]
    return layout

def get_word_ladder_gen_layout():
    layout = [[sg.Text('Select Difficulty Level', font=FONT)],
              [sg.Combo(LEVELS, auto_size_text=True, default_value=LEVELS[0], enable_events=True, key='-WLLEVEL-', font=FONT)],
              [sg.Button('SUBMIT', font=FONT)],
              [sg.Button('BACK', font=FONT)]]
    return layout

def get_word_ladder_layout(wordladdergenerator):
    chars = wordladdergenerator.wordchars
    start = wordladdergenerator.start
    end = wordladdergenerator.end
    depth = wordladdergenerator.depth
    layout = [[sg.Text(char, size=(4,1), justification='c', font=FONT) for char in start]]
    layout += [[sg.InputText(size=(3,1), justification='c', key=(row,col), font=FONT) for col in range(chars)] for row in range(depth)]
    layout += [[sg.Text(char, size=(4,1), justification='c', font=FONT) for char in end],
               [sg.Button('CHECK', font=FONT), sg.Button('HINT', font=FONT), sg.Button('SOLUTION', font=FONT)],[sg.Button('SUBMIT', font=FONT), sg.Button('NEXT', font=FONT)],
               [sg.Button('HELP', font=FONT), sg.Button('EXIT', font=FONT)]]
    return layout

def get_leaderboard_layout():
    layout = [[sg.Text('leaderboard', font=FONT)],
               [sg.Button('BACK', font=FONT)]]
    return layout

def get_separted_wordslist(wordslist):
    langwords = []
    englishwords = []
    for word in wordslist:
        langwords.append(word.split('  -  ')[0])
        englishwords.append(word.split('  -  ')[1])
    return langwords, englishwords


w, h = sg.Window.get_screen_size()

layout = [[sg.Button('WORD SEARCH', font=FONT)],
          [sg.Button('WORD LADDER', font=FONT)],
          [sg.Button('LEADERBOARD', font=FONT)],
          [sg.Button('EXIT', font=FONT)]]

win1 = sg.Window('Word Puzzle', layout, size=(h,480), element_justification='c', font=FONT)
win2_active = False
win3_active = False
wordsearch = False
wordladder = False
wordslist = []
wordsloc = []
firstchar = 0
wordsdict = []
wordsearch_dictionary = {}

        
while True:
    event1, values1 = win1.read(timeout=100)
            
    if event1 in (sg.WIN_CLOSED, 'EXIT'):
        break

    if not win2_active and event1 == 'WORD SEARCH':
        wordsearch = True
        win2_active = True
        win2 = sg.Window('Word Search Configuration', get_word_search_gen_layout(), size=(h,480), element_justification='c', font=FONT)

    if not win2_active and event1 == 'WORD LADDER':
        wordladder = True
        win2_active = True
        win2 = sg.Window('Word Ladder Configuration', get_word_ladder_gen_layout(), size=(h,480), element_justification='c', font=FONT)
                
    if not win2_active and event1 == 'LEADERBOARD':
        win2_active = True
        win2 = sg.Window('Leaderboard', get_leaderboard_layout(), size=(h,480), element_justification='c', font=FONT)
            
    if win2_active:
        event2, values2 = win2.read(timeout=100)
                
        if event2 in (sg.WIN_CLOSED, 'BACK'):         
            win2_active  = False
            wordsearch = False
            wordladder = False
            win2.close()
                    
        if not win3_active and event2 == 'SUBMIT':
            if wordsearch:
                wordsearch_dictionary = {
                    'lang': values2['-WSLANGUAGE-'],
                    'category': values2['-WSCATEGORY-'],
                    'grid_size': values2['-WSGRIDSIZE-']
                }
                grid = generate_word_search(wordsearch_dictionary)
                wordslist = grid.get_word_list()
                wordsloc = get_words_loc()
                row = int(grid.get_row())
                col = int(grid.get_col())

                win3_active = True
                win3 = sg.Window('Word Search', get_word_search_layout(row, col, wordslist), finalize=True, resizable=True, font=FONT)
                create_grid(win3, grid, wordsearch_dictionary)

                if wordsearch_dictionary['lang'] not in 'English':
                    wordslist, englishwords = get_separted_wordslist(wordslist)

            if wordladder:
                level = values2['-WLLEVEL-']
                wordladdergenerator = WordLadder(level)
                wordladdergenerator.selectSourceTargetWords()
                win3_active = True                
                win3 = sg.Window('Word Ladder', get_word_ladder_layout(wordladdergenerator), font=FONT)

            win2_active = False
            win2.close()

    if win3_active:
        event3, values3 = win3.read(timeout=1000)

        if event3 in (sg.WIN_CLOSED, 'EXIT'):
            wordladder = False
            wordsearch = False
            win3_active = False
            wordladdergenerator = None
            wordsdict.clear()
            found = False
            islast = False
            currentword = None
            win3.close()
            
        if win3_active and wordladder:
            wordsdict.clear()
            wordsdict.append(wordladdergenerator.start)
            for row in range(wordladdergenerator.depth):    
                word = ''
                for col in range(wordladdergenerator.wordchars):
                    char = str(values3[(row,col)])
                    if char.isalpha() and len(char) == 1:
                        word += char
                wordsdict.insert(row+1, word)
            wordsdict.append(wordladdergenerator.end)
            
            for index, word in enumerate(wordsdict):
                if word == '':
                    break
                elif word not in (wordladdergenerator.start, wordladdergenerator.end):
                    if len(word) == wordladdergenerator.wordchars and index == wordladdergenerator.wordcount:
                        found, islast = wordladdergenerator.checkInput(word)
                        if found:
                            currentword = word
                            break
                        
                            
            if 'CHECK' in event3:
                if not found:
                    text = 'Invalid word ' + word + '.\n\n' + word + ' does not exist from word ' + wordladdergenerator.currentstate + ' to ' + word
                    sg.Popup(text, title='Invalid Word', keep_on_top=True,text_color='Black', font=FONT)
                
            elif 'HINT' in event3:                
                word = wordladdergenerator.getNextWord()
                if word == wordladdergenerator.end:
                    sg.Popup('Please click SUBMIT after this pop up.')
                else:
                    col = 0
                    row = wordladdergenerator.wordcount-1
                    for char in word:
                        win3.Element((row, col)).Update(char)
                        col += 1
                    
            elif 'SOLUTION' in event3:
                if '' in wordsdict:
                    path = wordladdergenerator.getPath()
                    for word, row  in zip(path[1:], range(wordladdergenerator.depth)):
                        for char, col in zip(word, range(wordladdergenerator.wordchars)):
                            if word != wordladdergenerator.end:
                                win3.Element((row, col)).Update(char)
                            elif word == wordladdergenerator.end:
                                break
                else:
                    sg.Popup('Please click SUBMIT after this pop up.')       
                                  
            elif 'SUBMIT' in event3:
                try:
                    islast
                except NameError:
                    sg.Popup('Please enter all the words before clicking submit.', title='Error', keep_on_top=True,text_color='Black', font=FONT)
                else:
                    if islast:
                        sg.Popup('Congratulations you solved the puzzle.\n\nPlease click NEXT after this pop up for a new game.', title='Congratulations', keep_on_top=True,text_color='Black', font=FONT)
                    else:
                        sg.Popup('Please enter all the words before clicking submit.', title='Error', keep_on_top=True,text_color='Black', font=FONT)
                        
            elif 'NEXT' in event3:
                wordsdict.clear()
                currentword = None
                win3.close()
                wordladdergenerator.selectSourceTargetWords()           
                win3 = sg.Window('Word Ladder', get_word_ladder_layout(wordladdergenerator), font=FONT)
                
            elif 'HELP' in event3:
                sg.Popup('The goal of this game is to get from the start word to the end word by changing only one character at a time. Only one character are allowed in eahc box.\n\nCHECK\nCheck the correctness of each of the entered word\n\nSUBMIT\nCheck the correctness of the path.\n\nHINT\nDisplay the hint of the next word in the path.\n\nSOLUTION\nReveal all the words from start to end word.\n\nNEXT\nGenerate next puzzle with the same difficulty level.\n', title='Word Ladder Help Menu', keep_on_top=True, text_color='Black', font=FONT)
            
        if win3_active and wordsearch:     
            row = 0
            col = 0
            
            if 'SOLUTION' in event3:
                for row in wordsloc:
                    starti = row[1][0]
                    startj = row[1][1]
                    endi = row[2][0]
                    endj = row[2][1]
                    word = row[0]
                    tsi, tsj = starti, startj
                    if endi < starti:
                        temp = starti
                        starti = endi
                        endi = temp
                    if endj < startj:
                        temp = startj
                        startj = endj
                        endj = temp
                    if ((endi - starti + 1) == len(word)) or ((endj - startj + 1) == len(word)):
                        if (starti == endi) or (startj == endj):
                            find_word(win3, grid, starti, startj, endi, endj, True)
                        else:
                            find_word_di(win3, grid, tsi, tsj, word, True)
            
            elif 'HELP' in event3:
                text = 'Find all the words on the list in the grid.\n\nSOLUTION\nHighlight the not found words in gray colour.\n\nNEXT\nGenerate next puzzle with the same configuration.'
                sg.Popup(text, title='Word Search Help Menu', keep_on_top=True, text_color='Black', font=FONT)
            
            elif 'NEXT' in event3:
                win3.close()
                grid = generate_word_search(wordsearch_dictionary)
                wordslist = grid.get_word_list()
                wordsloc = get_words_loc()
                row = int(grid.get_row())
                col = int(grid.get_col())

                win3_active = True
                win3 = sg.Window('Word Search', get_word_search_layout(row, col, wordslist), finalize=True, resizable=True, font=FONT)
                create_grid(win3, grid, wordsearch_dictionary)
                
            if '-WSGRAPH-' in event3:
                mouse = values3['-WSGRAPH-']
                if mouse == (None, None):
                    continue
                if firstchar == 0:
                    start_j = mouse[0] // BOX_SIZE
                    start_i = mouse[1] // BOX_SIZE
                    start = grid.get(start_i, start_j)
                firstchar += 1
            if event3.endswith('+UP'):
                end_j = mouse[0] // BOX_SIZE
                end_i = mouse[1] // BOX_SIZE
                end = grid.get(end_i, end_j)
                firstchar = 0
                space = False
                hypen = False
                for word, row in zip(wordslist, wordsloc):
                    if " " in word:
                        space = True
                        ori_word = word
                        word = word.replace(" ", "")
                    elif "-" in word:
                        hypen = True
                        ori_word = word
                        word = word.replace("-", "")
                    if word.startswith(start) and word.endswith(end):
                        tsi, tsj = start_i, start_j
                        if end_i < start_i:
                            temp = start_i
                            start_i = end_i
                            end_i = temp
                        if end_j < start_j:
                            temp = start_j
                            start_j = end_j
                            end_j = temp
                        if ((end_i - start_i + 1) == len(word)) or ((end_j - start_j + 1) == len(word)):
                            if (end_i == start_i) or (end_j == start_j):
                                find_word(win3, grid, start_i, start_j, end_i, end_j, False)
                            else:
                                find_word_di(win3, grid, tsi, tsj, word, False)
                            if space or hypen:
                                wordslist.remove(ori_word)
                                wordsloc.remove(row)
                            else:
                                wordslist.remove(word)
                                wordsloc.remove(row)
                            break