import random
import PySimpleGUI as sg
import networkx as nx

from wordladder.graph import WordLadder
from wordsearch.generategrid import generate_word_search
from wordsearch.grid import Grid

LANGUAGES = ['English', 'Irish', 'French', 'German', 'Spanish', 'Italian']
CATEGORIES = ['animals', 'careers', 'colours', 'countries', 'emotions', 'flowers', 'fruits', 'human body', 'shapes', 'sports', 'vegetables']
GRID_SIZE = ['12x12', '15x15', '17x17', '20x20', '22x22', '25x25', '27x27']
LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Master']
COLOURS = ['blue', 'yellow', 'light pink', 'orange', 'lime', 'cyan']

BOX_SIZE = 25
BOX_PAD = 2.5


def create_grid(win3, grid, wordsearch_dictionary):
    sizes = wordsearch_dictionary['grid_size'].split('x')

    g = win3['-WSGRAPH-']
    for row in range(int(sizes[0])):
        for col in range(int(sizes[1])):
            g.draw_rectangle((col * BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_PAD),
                             (col * BOX_SIZE + BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             line_color='black')
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 15.5, row * BOX_SIZE + 15.5),
                       font=("Ariel", 12))


def find_word(win3, grid, start_i, start_j, end_i, end_j):
    g = win3['-WSGRAPH-']
    colour = random.choice(COLOURS)
    for row in range(start_i, end_i + 1):
        for col in range(start_j, end_j + 1):
            g.draw_rectangle((col * BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_PAD),
                             (col * BOX_SIZE + BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 15.5, row * BOX_SIZE + 15.5),
                       font=("Ariel", 12))


def find_word_di(win3, grid, start_i, start_j, word):
    word = list(word)
    g = win3['-WSGRAPH-']
    colour = random.choice(COLOURS)
    
    i, j, found = grid.check_avail_di_left_down(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Ariel", 12))
            i += 1
            j += 1
            found = False
        
    i, j, found = grid.check_avail_di_left_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Ariel", 12))
            i -= 1
            j += 1
            found = False
                
    i, j, found = grid.check_avail_di_right_down(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Ariel", 12))
            i += 1
            j -= 1
            found = False
            
    i, j, found = grid.check_avail_di_right_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 15.5, i * BOX_SIZE + 15.5), font=("Ariel", 12))
            i -= 1
            j -= 1
            found = False
            
def get_word_search_gen_layout():
    layout = [[sg.Text('Select Language')],
              [sg.Combo(LANGUAGES, auto_size_text=True, default_value=LANGUAGES[0], enable_events=True, key='-WSLANGUAGE-')],
              [sg.Text('Select Category')],
              [sg.Combo(CATEGORIES, auto_size_text=True, default_value=CATEGORIES[0], enable_events=True, key='-WSCATEGORY-')],
              [sg.Text('Enter Grid Size')],
              [sg.Combo(GRID_SIZE, auto_size_text=True, default_value=GRID_SIZE[0], enable_events=True, key='-WSGRIDSIZE-')],
              [sg.Button('SUBMIT')],
              [sg.Button('EXIT')]]
    return layout

def get_word_search_layout(row, col, wordslist):
    words = '\n'.join(wordslist)
    layout = [
        [sg.Graph((BOX_SIZE * row + 10, BOX_SIZE * col + 10), (0, BOX_SIZE * row + 10), (BOX_SIZE * col + 10, 0), background_color='white', key='-WSGRAPH-', enable_events=True, drag_submits=True), 
         sg.VerticalSeparator(),
         sg.Text(words, key='-WSLIST-')],
        [sg.Button('EXIT')]]
    return layout

def get_word_ladder_gen_layout():
    layout = [[sg.Text('Select Difficulty Level')],
              [sg.Combo(LEVELS, auto_size_text=True, default_value=LEVELS[0], enable_events=True, key='-WLLEVEL-')],
              [sg.Button('SUBMIT')],
              [sg.Button('EXIT')]]
    return layout

# 0 - 'Beginner'
# 1 - 'Intermediate'
# 2 - 'Advanced'
# 3 - 'Master'
# 7 Layers of input box with visible setting changes
def get_word_ladder_layout(wordladdergenerator):
    
    layout = [[sg.Text('Word ladder game play')],
              # [sg.Graph(())]
              [sg.Text()],
              [sg.InputText()]
              [sg.Button('SOLUTION'), sg.Button('HINT'), sg.Button('NEXT'), sg.Button('EXIT')]]
    return layout

def get_leaderboard_layout():
    layout = [[sg.Text('leaderboard')],
               [sg.Button('EXIT')]]
    return layout

def get_separted_wordslist(wordslist):
    langwords = []
    englishwords = []
    for word in wordslist:
        langwords.append(word.split('  -  ')[0])
        englishwords.append(word.split('  -  ')[1])
    return langwords, englishwords



print(sg.Window.get_screen_size())
w, _ = sg.Window.get_screen_size()
layout = [[sg.Button('WORD SEARCH'), sg.Button('WORD LADDER')],
          [sg.Button('LEADERBOARD'), sg.Button('EXIT')]]

win1 = sg.Window('Word Puzzle', layout)
win2_active = False
win3_active = False
wordsearch = False
wordladder = False
wordslist = []
firstchar = 0
        
while True:
    event1, values1 = win1.read(timeout=100)
    print(event1, values1)
            
    if event1 in (sg.WIN_CLOSED, 'EXIT'):
        break

    if not win2_active and event1 == 'WORD SEARCH':
        wordsearch = True
        win2_active = True
        win2 = sg.Window('Word Search Configuration', get_word_search_gen_layout())

    if not win2_active and event1 == 'WORD LADDER':
        wordladder = True
        win2_active = True
        win2 = sg.Window('Word Ladder Configuration', get_word_ladder_gen_layout())
                
    if not win2_active and event1 == 'LEADERBOARD':
        win2_active = True
        win2 = sg.Window('Leaderboard', get_leaderboard_layout())
            
    if win2_active:
        event2, values2 = win2.read(timeout=100)
                
        if event2 in (sg.WIN_CLOSED, 'EXIT'):         
            win2_active  = False
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
                row = int(grid.get_row())
                col = int(grid.get_col())

                win3_active = True
                win3 = sg.Window('Word Search', get_word_search_layout(row, col, wordslist), finalize=True, resizable=True)
                create_grid(win3, grid, wordsearch_dictionary)

                if wordsearch_dictionary['lang'] not in 'English':
                    wordslist, englishwords = get_separted_wordslist(wordslist)

            if wordladder:
                level = values2['-WLLEVEL-']
                wordladdergenerator = WordLadder(level)
                wordladdergenerator.selectSourceTargetWords()
                
                win3_active = True                
                win3 = sg.Window('Word Ladder', get_word_ladder_layout(wordladdergenerator))

            win2_active = False
            win2.close()

    if win3_active:
        event3, values3 = win3.read(timeout=3000)

        if event3 in (sg.WIN_CLOSED, 'EXIT'):
            wordladder = False
            wordsearch = False
            win3_active = False
            wordladdergenerator = None
            win3.close()
            
        if win3_active and 'NEXT' in event3:
            pass

        if win3_active and '-WSGRAPH-' in event3:
            mouse = values3['-WSGRAPH-']
            if mouse == (None, None):
                continue
            if firstchar == 0:
                start_j = mouse[0] // BOX_SIZE
                start_i = mouse[1] // BOX_SIZE
                start = grid.get(start_i, start_j)
            firstchar += 1
        if win3_active and event3.endswith('+UP'):
            end_j = mouse[0] // BOX_SIZE
            end_i = mouse[1] // BOX_SIZE
            end = grid.get(end_i, end_j)

            firstchar = 0
            space = False
            hypen = False
            for word in wordslist:
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
                            find_word(win3, grid, start_i, start_j, end_i, end_j)
                        else:
                            find_word_di(win3, grid, tsi, tsj, word)
                        if space or hypen:
                            wordslist.remove(ori_word)
                        else:
                            wordslist.remove(word)
                        break
