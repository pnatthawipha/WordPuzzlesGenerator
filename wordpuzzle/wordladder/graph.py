import networkx as nx
import json
import random
import enchant
from .twl import check
from collections import defaultdict
from itertools import product

LEVELS = {
        'Beginner': 4,
        'Intermediate': 5,
        'Advanced': 6,
        'Master': 7
    }

class WordLadder :
    
    def __init__(self, level):
        self.level = level
        self.wordchars = LEVELS.get(level)
        self.wordslist = self.getWords(self.wordchars)
        self.paths = self.getPaths(self.wordchars)
        self.start = None
        self.end = None
        self.depth = None
        self.wordcount = None
        self.currentstate = None

    def read_words_file(self):
        d = enchant.Dict('en_IE')
        with open('C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\graphs\\allwords.txt', 'r') as file:
            dictionary = set(file.read().split())
            words = defaultdict(list)
            
            for i in range(4): # 4-7
                for word in dictionary:
                    if i+4 == len(word) and d.check(word) and check(word):
                        words[i+4].append(word)
            return words
                    
    def build_graph(self):
        words = self.read_words_file()
        
        for i in range(4):
            G = nx.Graph()
            buckets = defaultdict(list)

            # add words that differs by one letter into the same bucket
            for word in words[i+4]:
                for j in range(len(word)):
                    bucket = '{}_{}'.format(word[:j], word[j + 1:])
                    buckets[bucket].append(word)

            # add vertices and edges for words in the same bucket
            for bucket, mutual_neighbors in buckets.items():
                for word1, word2 in product(mutual_neighbors, repeat=2):
                    if word1 != word2:
                        G.add_edge(word1, word2)
            
            filename = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\graphs\\graphs_' + str(i+4) + '.graphml'
            nx.write_graphml(G, filename)
            file = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\graphs\\usedwords' + str(i+4) + '.txt'
            f = open(file, 'w+')
            f.write("%s" % '\n'.join(list(G.nodes)))
            f.close()        

    def dumpToFile(self):
        for i in range(4,8):
            G = self.load_graph(i)
            paths = dict(nx.all_pairs_shortest_path(G, 6))
            with open('C:\\Users\\peung\\Desktop\\FYP\\src\\paths' + str(i) + '.json', 'w') as f:
                json.dump(paths, f)

    def load_graph(self, wordchars):
        file = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\graphs\\graphs_' + str(wordchars) + '.graphml'
        graph = nx.read_graphml(file)
        return graph

    def getWords(self, wordchars):
        file = 'C:\\Workarea\\GitHub\\WordPuzzlesGenerator\\wordpuzzle\\data\\graphs\\usedwords' + str(wordchars) + '.txt'
        with open(file, 'r') as f:
            return f.read().split()
            
    def getPaths(self, wordchars):
        file = 'C:\\Users\\peung\\Desktop\\FYP\\src\\paths' + str(wordchars) + '.json'
        with open(file, 'r') as f:
            return json.load(f)

    def changeLevel(self, level):
        if level not in self.level:
            self.level = level
            self.wordchars = LEVELS.get(level)
            self.wordslist = self.getWords(self.wordchars)
            self.paths = self.getPaths(self.wordchars)
            self.start = None
            self.end = None
            self.depth = None
            self.wordcount = None
            self.currentstate = None

    def selectSourceTargetWords(self):
        found = False
        while not found:
            start = random.choice(self.wordslist)
            end = random.choice(self.wordslist)
            if start in self.paths[start]:
                if end in self.paths[start]:
                    print(self.paths[start][end])
                    length = len(self.paths[start][end])
                    if length <= 7 and length > 2:
                        self.start = start
                        self.end = end
                        self.currentstate = start
                        self.depth = length-2
                        self.wordcount = 1
                        found = True
            
    def checkInput(self, word):
        d = enchant.Dict('en_IE')
        found = False
        isLast = False
        if d.check(word) and check(word):
            if word in self.paths[self.currentstate][word] and len(self.paths[self.currentstate][word]) == 2: 
                if len(self.paths[word][self.end]) == 2:
                    self.currentstate = word
                    self.wordcount += 1
                    found = True
                    isLast = True
                elif self.wordcount < self.depth + 1:
                    self.currentstate = word
                    self.wordcount += 1
                    found = True               
        return found, isLast
    
    def getNextWord(self):
        #try:
        paths = self.paths[self.currentstate][self.end]
        return paths[1]
        #exception
        #if word in self.paths[self.currentstate][self.end]:
            
    def getPath(self):
        return self.paths[self.start][self.end]
        
                
                