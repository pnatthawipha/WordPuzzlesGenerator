import numpy as np
import random

class Grid:    
    def __init__(self, row, col, wordslist):
        self.row = row
        self.col = col
        self.wordslist = wordslist
        self.matrix = np.zeros((row, col))
        self.matrix = self.matrix.astype(str)

    def print_grid(self):
        for i in range(self.row):
            for j in range(self.col):
                print(self.matrix[i][j], end=" ")
            print()

    def fill_in_blanks(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] in '0.0':
                    self.matrix[i][j] = '-'
        return self.matrix
    
    def fill_in_blanks(self, characters):
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] in '0.0':
                    self.matrix[i][j] = random.choice(characters)
        return self.matrix
    
    def get(self, i, j):
        return self.matrix[i][j]

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col
    
    def get_word_list(self):
        return self.wordslist

    def add_word_list(self, wordslist):
        self.wordslist = wordslist
    
    def check_avail_hor_right(self, row, col, word):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            i = random.randint(0, row-1)
            j = random.randint(len(word)-1, col-1)
            ti, tj = i, j
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    j -= 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_hor_left(self, row, col, word):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            i = random.randint(0, row-1)
            j = random.randint(0, col-len(word)-1)
            ti, tj = i, j
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    j += 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break
        
    def check_avail_ver_up(self, row, col, word):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            i = random.randint(len(word)-1, row-1)
            j = random.randint(0, col-1)
            ti, tj = i, j
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i -= 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_ver_down(self, row, col, word):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            i = random.randint(0, row-len(word)-1)
            j = random.randint(0, col-1)
            ti, tj = i, j
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i += 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_di_left_down(self, row, col, word, check):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            if check:
                i = random.randint(0, row-len(word)-1)
                j = random.randint(0, col-len(word)-1)
                ti, tj = i, j
            else:
                if row > (self.get_row()-len(word)-1) or col > (self.get_col()-len(word)-1):
                    return row, col, False
                i, j = row, col
                ti, tj = row, col
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i += 1
                    j += 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_di_left_up(self, row, col, word, check):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            if check:
                i = random.randint(len(word)-1, row-1)
                j = random.randint(0, col-len(word)-1)
                ti, tj = i, j
            else:
                if row < len(word)-1 or col > (self.get_col()-len(word)-1):
                    return row, col, False
                i, j = row, col
                ti, tj = row, col
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i -= 1
                    j += 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_di_right_down(self, row, col, word, check):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            if check:
                i = random.randint(0, row-len(word)-1)
                j = random.randint(len(word)-1, col-1)
                ti, tj = i, j
            else:
                if row > (self.get_row()-len(word)-1) or col < len(word)-1:
                    return row, col, False
                i, j = row, col
                ti, tj = row, col
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i += 1
                    j -= 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break

    def check_avail_di_right_up(self, row, col, word, check):
        word = list(word)
        
        notfoundcount = 0
        while not False:
            if check:
                i = random.randint(len(word)-1, row-1)
                j = random.randint(len(word)-1, col-1)
                ti, tj = i, j
            else:
                if row < len(word)-1 or col < len(word)-1:
                    return row, col, False
                i, j = row, col
                ti, tj = row, col
            for k in range(len(word)):
                if '0.0' in self.matrix[i][j] or (word[k] == self.matrix[i][j]):
                    i -= 1
                    j -= 1
                    if k == len(word) - 1:
                        return ti, tj, True
                else:
                    notfoundcount += 1
                    if notfoundcount >= max(row, col):
                        return ti, tj, False
                    break        
    
    def add_hor_left(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            j += 1
        return i, j-1
    
    def add_hor_right(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            j -= 1
        return i, j+1
    
    def add_ver_up(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            i -= 1
        return i+1, j
            
    def add_ver_down(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            i += 1
        return i-1, j
    
    def add_di_left_down(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            i += 1
            j += 1
        return i-1, j-1
    
    def add_di_left_up(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            i -= 1
            j += 1    
        return i+1, j-1
    
    def add_di_right_down(self, word, i, j):
        for ch in word:
            self.matrix[i][j] = ch
            i += 1
            j -= 1  
        return i-1, j+1
    
    def add_di_right_up(self, word, i, j): 
        for ch in word:
            self.matrix[i][j] = ch
            i -= 1
            j -= 1
        return i+1, j+1
        
    
    def execute_add_word(self, argument, word, i, j):
        switcher = {
            'hor-left':self.add_hor_left,
            'hor-right':self.add_hor_right,
            'ver-down':self.add_ver_down,
            'ver-up':self.add_ver_up,
            'di-left-down':self.add_di_left_down,
            'di-left-up':self.add_di_left_up,
            'di-right-down':self.add_di_right_down,
            'di-right-up':self.add_di_right_up
        }
        return switcher[argument](word, i, j)

    def add_word(self, word, i, j, direction):
        return self.execute_add_word(direction, word, i, j)