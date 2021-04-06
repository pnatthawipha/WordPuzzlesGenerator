import random
from tkinter import font
import PySimpleGUI as sg
import numpy as np

from wordladder.graph import WordLadder
from wordsearch.generategrid import generate_word_search, get_words_loc
from wordsearch.grid import Grid

LANGUAGES = ['English', 'Irish', 'French', 'German', 'Spanish', 'Italian']
CATEGORIES = ['animals', 'careers', 'colours', 'emotions', 'flowers', 'fruits', 'greek gods', 'sports', 'vegetables']
GRID_SIZE = ['15x15', '17x17', '20x20', '22x22', '25x25', '27x27']
LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Master']
COLOURS = ['blue', 'yellow', 'light pink', 'orange', 'lime', 'cyan']

BOX_SIZE = 27.5
BOX_PAD = 2.5
FONT = ('Helvetica',14)

MAX_ROWS = MAX_COLS = 7


def create_grid(win3, grid, wordsearch_dictionary):
    sizes = wordsearch_dictionary['grid_size'].split('x')

    g = win3['-WSGRAPH-']
    for row in range(int(sizes[0])):
        for col in range(int(sizes[1])):
            g.draw_rectangle((col * BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_PAD),
                             (col * BOX_SIZE + BOX_SIZE + BOX_PAD, row * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             line_color='black')
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 17, row * BOX_SIZE + 17),
                       font=FONT)


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
            g.DrawText('{}'.format(grid.get(row, col)), (col * BOX_SIZE + 17, row * BOX_SIZE + 17),
                       font=FONT)

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
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 17, i * BOX_SIZE + 17), font=FONT)
            i += 1
            j += 1
            found = False
        
    i, j, found = grid.check_avail_di_left_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 17, i * BOX_SIZE + 17), font=FONT)
            i -= 1
            j += 1
            found = False
                
    i, j, found = grid.check_avail_di_right_down(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 17, i * BOX_SIZE + 17), font=FONT)
            i += 1
            j -= 1
            found = False
            
    i, j, found = grid.check_avail_di_right_up(start_i, start_j, word, False)
    if found:
        for _ in word:
            g.draw_rectangle((j * BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_PAD),
                             (j * BOX_SIZE + BOX_SIZE + BOX_PAD, i * BOX_SIZE + BOX_SIZE + BOX_PAD),
                             fill_color=colour)
            g.DrawText('{}'.format(grid.get(i,j)), (j * BOX_SIZE + 17, i * BOX_SIZE + 17), font=FONT)
            i -= 1
            j -= 1
            found = False
            
def get_word_search_gen_layout():
    secondcol = [[sg.Text(' ', key='-OUTPUT-', font=FONT, size=(25,2))],
                 [sg.Button(button_text='SELECT FILE', font=FONT)]]
    firstcol = [[sg.Text('Select Language', font=FONT)],
                 [sg.Combo(LANGUAGES, auto_size_text=True, enable_events=True, key='-WSLANGUAGE-', font=FONT)],
                 [sg.Text('Select Category')],
                 [sg.Combo(CATEGORIES, auto_size_text=True, enable_events=True, key='-WSCATEGORY-', font=FONT)]]
    layout = [[sg.Text('Select the grid size and either select a file or select the language and category.\nThe file must contain the a list of words seperated by newlines.\n', font=FONT)],
              [sg.Text('Enter Grid Size')],
              [sg.Combo(GRID_SIZE, auto_size_text=True, default_value=GRID_SIZE[0], enable_events=True, key='-WSGRIDSIZE-', font=FONT)]]
    layout += [[sg.Column(firstcol),
                sg.VerticalSeparator(),
                sg.Column(secondcol)]]
    layout += [[sg.Button('SUBMIT', font=FONT)],
               [sg.Button('BACK', font=FONT)]]
    return layout

def get_word_search_layout(row, col, wordslist):
    if '  -  ' in wordslist[0]:
        _, engwords = get_separted_wordslist(wordslist)
        secondcol = [[sg.Text(word, key=kword, font=('Helvetica',13), text_color='Black', pad=(0,0), justification='c', size=(40,1))] for kword, word in zip(engwords, wordslist)]
    else:
        secondcol = [[sg.Text(word, key=word, font=('Helvetica',13), text_color='Black', pad=(0,0), justification='c', size=(40,1))] for word in wordslist]
    firstcol = [[sg.Graph((BOX_SIZE * row + 10, BOX_SIZE * col + 10), (0, BOX_SIZE * row + 10), (BOX_SIZE * col + 10, 0), background_color='white', key='-WSGRAPH-', enable_events=True, drag_submits=True)]]
    
    layout = [[sg.Text('Find all the words in the grid. Click and drag the mouse from first character of the word to the last character of the word and let go to select the word.', font=('Helvetica',13))],
              [sg.Column(firstcol),
               sg.VerticalSeparator(),
               sg.Column(secondcol)],
              [sg.Button('SOLUTION', font=FONT), sg.Button('HELP', font=FONT), sg.Button('NEXT', font=FONT), sg.Button('EXIT', font=FONT)]]
    return layout

def get_word_ladder_gen_layout():
    layout = [[sg.Text('Select Difficulty Level', font=FONT)],
              [sg.Combo(LEVELS, auto_size_text=True, default_value=LEVELS[0], enable_events=True, key='-WLLEVEL-', font=FONT)],
              [sg.Button('SUBMIT', font=FONT)],
              [sg.Button('BACK', font=FONT)]]
    return layout

def get_word_ladder_layout(wlgenerator):
    chars = wlgenerator.wordchars
    start = wlgenerator.start
    end = wlgenerator.end
    depth = wlgenerator.depth
    layout = [[sg.Text('The goal of this game is to get from the start word to the end word by changing only one character at a time. Only one character are allowed in each box.\n\n', font=('Helvetica',14), text_color='Black')]]
    layout += [[sg.Text(char, size=(3,1), justification='c', font=('Helvetica',16), text_color='Black') for char in start]]
    layout += [[sg.InputText(size=(3,2), justification='c', key=(row,col), font=('Helvetica',16)) for col in range(chars)] for row in range(depth)]
    layout += [[sg.Text(char, size=(3,2), justification='c', font=('Helvetica',16), text_color='Black') for char in end],
               [sg.Button('CHECK', font=FONT), sg.Button('HINT', font=FONT), sg.Button('SOLUTION', font=FONT)],[sg.Button('SUBMIT', font=FONT), sg.Button('NEXT', font=FONT), sg.Button('RESET', font=FONT)],
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

def check_unique(words):
    if np.unique(words).size() == len(words):
        return True
    else:
        return False
 
w, h = sg.Window.get_screen_size()

layout = [[sg.Button('WORD SEARCH', font=('Helvetica',20))],
          [sg.Button('WORD LADDER', font=('Helvetica',20))],
          [sg.Button('LEADERBOARD', font=('Helvetica',20))],
          [sg.Button('EXIT', font=('Helvetica',20))]]

win1 = sg.Window('Word Puzzle', layout, size=(h,480), element_justification='c')
win2_active = False
win3_active = False
wordsearch = False
wordladder = False
wordslist = []
wordsloc = []
firstchar = 0
wordsdict = []
wordsearch_dictionary = {}
wscomplete = False

        
while True:
    event1, values1 = win1.read(timeout=100)
            
    if event1 in (sg.WIN_CLOSED, 'EXIT'):
        break

    if not win2_active and event1 == 'WORD SEARCH':
        wordsearch = True
        win2_active = True
        win2 = sg.Window('Word Search Configuration', get_word_search_gen_layout(), size=(w,h), element_justification='c', font=FONT, no_titlebar=True, location=(0, 0))

    if not win2_active and event1 == 'WORD LADDER':
        wordladder = True
        win2_active = True
        win2 = sg.Window('Word Ladder Configuration', get_word_ladder_gen_layout(), size=(w,h), element_justification='c', font=FONT, no_titlebar=True, location=(0, 0))
                
    if not win2_active and event1 == 'LEADERBOARD':
        win2_active = True
        win2 = sg.Window('Leaderboard', get_leaderboard_layout(), size=(h,480), element_justification='c', font=FONT)
            
    if win2_active:
        event2, values2 = win2.read(timeout=100)
                
        if event2 in (sg.WIN_CLOSED, 'BACK'):         
            win2_active  = False
            wordsearch = False
            wordladder = False
            wordsearch_dictionary.clear()
            win2.close()
            
        if event2 and 'SELECT FILE' in event2:
            fname = sg.popup_get_file('Document to open')
            sentence = 'The selected file is:\n' + fname
            win2.Element('-OUTPUT-').Update(sentence)
        
        if event2 == 'HELP' and wordsearch:
            sg.Popup('')

        if not win3_active and event2 == 'SUBMIT':
            if wordsearch:
                try:
                    fname
                except NameError:
                    wordsearch_dictionary = {
                        'lang': values2['-WSLANGUAGE-'],
                        'category': values2['-WSCATEGORY-'],
                        'grid_size': values2['-WSGRIDSIZE-']
                    }
                    lang = values2['-WSLANGUAGE-']
                    readfile = True
                    
                else:
                    lang = 'English'
                    readfile = False
                    wordsearch_dictionary = {
                        'grid_size': values2['-WSGRIDSIZE-'],
                        'file': fname
                    }
                try:
                    grid = generate_word_search(wordsearch_dictionary, readfile)
                except FileNotFoundError:
                    sg.Popup('Please provide one of the following combination in the Word Ladder Configuration Menu:\n* grid size and file input\n* grid size, category and language\n', font=FONT)
                else:
                    wordslist = grid.get_word_list()    
                    wordsloc = get_words_loc()
                    row = int(grid.get_row())
                    col = int(grid.get_col())
                    win3_active = True
                    win3 = sg.Window(title='', layout=get_word_search_layout(row, col, wordslist), finalize=True, resizable=True, element_justification='c', size=(w,h), no_titlebar=True, location=(0, 0))
                    create_grid(win3, grid, wordsearch_dictionary)
                
            if wordladder:
                level = values2['-WLLEVEL-']
                wlgenerator = WordLadder(level)
                wlgenerator.selectSourceTargetWords()
                win3_active = True                
                win3 = sg.Window(title='', layout=get_word_ladder_layout(wlgenerator), size=(w,h), element_justification='c', no_titlebar=True, location=(0, 0))

            win2_active = False
            win2.close()

    if win3_active:
        event3, values3 = win3.read(timeout=750)

        if event3 in (sg.WIN_CLOSED, 'EXIT'):
            wordladder = False
            wordsearch = False
            win3_active = False
            wscomplete = False
            readfile = None
            wordslist.clear()
            wordsdict.clear()
            try:
                fname
            except NameError:
                pass
            else:
                del fname
            wlgenerator = None
            found = False
            islast = False
            unfound = None
            win3.close()
            
        if win3_active and wordladder:
            wordsdict.clear()
            wordsdict.append(wlgenerator.start)
            for row in range(wlgenerator.depth):    
                word = ''
                for col in range(wlgenerator.wordchars):
                    char = str(values3[(row,col)])
                    if char.isalpha() and len(char) == 1:
                        word += char
                wordsdict.insert(row+1, word)
            wordsdict.append(wlgenerator.end)
            
            for index, word in enumerate(wordsdict):
                if word == '':
                    break
                elif word not in (wlgenerator.start, wlgenerator.end):
                    if len(word) == wlgenerator.wordchars and index == wlgenerator.wordcount:
                        found, islast = wlgenerator.checkInput(word)
                        if found:
                            islast = islast
                            break
                        
            if 'CHECK' in event3:
                try:
                    found
                except NameError:
                    sg.Popup('Please enter one word before clicking CHECK.', title='Error', keep_on_top=True, text_color='Black', font=FONT)
                else:
                    if not found:
                        text = 'Invalid word.'
                        sg.Popup(text, title='Invalid Word', keep_on_top=True,text_color='Black', font=FONT)
                
            elif 'HINT' in event3:
                if '' in wordsdict:
                    hint = wlgenerator.getNextWord()
                    if hint != None:
                        try:
                            found
                        except NameError:
                            pass
                        finally:
                            if wlgenerator.depth+1 >= len(wlgenerator.paths[wlgenerator.currentstate][wlgenerator.end])-1:
                                col = 0
                                row = wlgenerator.wordcount-1
                                wlgenerator.currentstate = hint
                                wlgenerator.wordcount += 1
                                for char in hint:
                                    found = True
                                    win3.Element((row, col)).Update(char)
                                    col += 1
                                if wlgenerator.getNextWord() == wlgenerator.end:
                                    islast = True
                            else:
                                sg.Popup('No word from ' + wlgenerator.currentstate + ' to ' + wlgenerator.end + '.', title='HINT', keep_on_top=True,text_color='Black', font=FONT)
                    else:
                        sg.Popup('No word from ' + wlgenerator.currentstate + ' to ' + wlgenerator.end + '.', title='HINT', keep_on_top=True,text_color='Black', font=FONT)
                else:
                    sg.Popup('Please click SUBMIT after this pop up.', title='HINT', keep_on_top=True,text_color='Black', font=FONT)
                                   
            elif 'SOLUTION' in event3:
                if '' in wordsdict:
                    for index, word in enumerate(wordsdict[1:]):
                        if word == wlgenerator.end:
                            break
                        elif word != '':
                            wlgenerator.currentstate = word
                            wlgenerator.wordcount += 1
                        elif word == '':
                            nextword = wlgenerator.getNextWord()
                            if nextword != None:
                                wlgenerator.currentstate = nextword
                                wlgenerator.wordcount += 1
                                wordsdict.insert(index, nextword)
                if wlgenerator.checkPath(wordsdict):
                    for word, row  in zip(wordsdict[1:], range(wlgenerator.depth+1)):
                        for char, col in zip(word, range(wlgenerator.wordchars)):
                            if word != wlgenerator.end:
                                win3.Element((row, col)).Update(char)
                    islast, found = True, True
                    sg.Popup('Please click NEXT after this pop up.', title='SOLUTION', keep_on_top=True,text_color='Black', font=FONT)
                else:
                    wlgenerator.currentstate = wlgenerator.start
                    wlgenerator.wordcount = 1
                    path = wlgenerator.getPath()
                    for word, row  in zip(path[1:], range(wlgenerator.depth+1)):
                        for char, col in zip(word, range(wlgenerator.wordchars)):
                            if word != wlgenerator.end:
                                win3.Element((row, col)).Update(char)
                                wlgenerator.wordcount += 1
                                found = True
                            elif word == wlgenerator.end:
                                islast = True
                                break
                    sg.Popup('Please click NEXT after this pop up.', title='SOLUTION', keep_on_top=True,text_color='Black', font=FONT)
                                  
            elif 'SUBMIT' in event3:
                if wlgenerator.checkPath(wordsdict):
                    if islast:
                        sg.Popup('Congratulations you solved the puzzle.\n\nPlease click NEXT after this pop up for a new game.', title='Congratulations', keep_on_top=True,text_color='Black', font=FONT)
                else:
                    sg.Popup('Please enter all the words correctly.', title='Error', keep_on_top=True,text_color='Black', font=FONT)
                        
            elif 'NEXT' in event3:
                wordsdict.clear()
                islast = None
                found = None
                pathfound = None
                win3.close()
                wlgenerator.selectSourceTargetWords()           
                win3 = sg.Window(title='', layout=get_word_ladder_layout(wlgenerator), size=(w,h), element_justification='c', no_titlebar=True, location=(0, 0))
                
            elif 'RESET' in event3:
                for row  in range(wlgenerator.depth):
                    for col in range(wlgenerator.wordchars):
                        if word != wlgenerator.end:
                            win3.Element((row, col)).Update('')
                wordsdict.clear()
                wlgenerator.reset()
                found = None
                islast = None
                pathfound = None
                
            elif 'HELP' in event3:
                sg.Popup('CHECK\nCheck the correctness of each of the entered word\n\nSUBMIT\nCheck the correctness of the path.\n\nHINT\nDisplay the hint of the next word in the path.\n\nSOLUTION\nReveal all the words from start to end word.\n\nNEXT\nGenerate next puzzle with the same difficulty level.\n', title='Word Ladder Help Menu', keep_on_top=True, text_color='Black', font=FONT)
            
        if win3_active and wordsearch:     
            row = 0
            col = 0
            
            if wscomplete:
                sg.Popup('Congratulations.\n\nYou completed the word search.\nPlease click next after this popup or exit and create a new word search.', title='Congratulations', keep_on_top=True,text_color='Black', font=FONT)
                wscomplete = False
            
            if 'SOLUTION' in event3:
                for row, kword in zip(wordsloc, wordslist):
                    starti = row[1][0]
                    startj = row[1][1]
                    endi = row[2][0]
                    endj = row[2][1]
                    if '  -  ' in kword:
                        word = kword.split('  -  ')[0]
                        if ' ' in word:
                            word = word.replace(" ", "")
                    else:
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
                        if '  -  ' in kword:
                            win3.Element(kword.split('  -  ')[1]).Update(kword, text_color='Red')
                        else:
                            win3.Element(kword).Update(kword, text_color='Red')        
                wordsloc.clear()
                wordslist.clear()
                if len(wordslist) == 0:
                    wscomplete = True
                    
            elif 'HELP' in event3:
                text = 'Find all the words on the list in the grid.\n\nSOLUTION\nHighlight the not found words in gray colour.\n\nNEXT\nGenerate next puzzle with the same configuration.'
                sg.Popup(text, title='Word Search Help Menu', keep_on_top=True, text_color='Black', font=FONT)
            
            elif 'NEXT' in event3:
                win3.close()
                wscomplete = False
                grid = generate_word_search(wordsearch_dictionary, readfile)
                wordslist = grid.get_word_list()
                wordsloc = get_words_loc()
                row = int(grid.get_row())
                col = int(grid.get_col())

                win3_active = True
                win3 = sg.Window(title='', layout=get_word_search_layout(row, col, wordslist), finalize=True, resizable=True, element_justification='c', size=(w,h), no_titlebar=True, location=(0, 0))
                create_grid(win3, grid, wordsearch_dictionary)
                
            if '-WSGRAPH-' in event3:
                mouse = values3['-WSGRAPH-']
                if mouse == (None, None):
                    continue
                if firstchar == 0:
                    start_j = int(mouse[0] // BOX_SIZE)
                    start_i = int(mouse[1] // BOX_SIZE)
                    start = grid.get(start_i, start_j)
                firstchar += 1
            if event3.endswith('+UP'):
                end_j = int(mouse[0] // BOX_SIZE)
                end_i = int(mouse[1] // BOX_SIZE)
                end = grid.get(end_i, end_j)
                firstchar = 0
                space = False
                hypen = False
                for word, row in zip(wordslist, wordsloc):
                    ori_word = word
                    if lang != 'English':
                        kword = word.split("  -  ")[1]
                        word = word.split("  -  ")[0]
                    else:
                        kword = word
                    if " " in word:
                        space = True
                        word = word.replace(" ", "")
                    elif "-" in word:
                        hypen = True
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
                                win3.Element(kword).Update(ori_word, text_color='Grey')
                            else:
                                if lang != 'English':
                                    wordslist.remove(ori_word)
                                else:
                                    wordslist.remove(word)
                                wordsloc.remove(row)
                                win3.Element(kword).Update(ori_word, text_color='Grey')
                            if len(wordslist) == 0:
                                wscomplete = True
                            break    