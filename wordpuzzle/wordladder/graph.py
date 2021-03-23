import networkx as nx
import json
import random
import enchant
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
        self.graph = self.load_graph(self.wordchars)
        self.wordslist = self.getWords(self.wordchars)
        self.paths = self.getPaths(self.wordchars)
        self.start = None
        self.end = None
        self.currentpath = []
        self.currentstate = None

    def read_words_file(self):
        d = enchant.Dict('en_IE')
        with open('C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\allwords.txt') as file:
            dictionary = set(file.read().split())
            words = defaultdict(list)
            
            for i in range(4): # 4-7
                for word in dictionary:
                    if i+4 == len(word) and d.check(word):
                        words[i+4].append(word)
            return words
                    
    def build_graph(self):
        words = self.read_words_file()
        # graph = nx.Graph()
        
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
            
            # graph = nx.union(G, graph)
            filename = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\graphs_' + str(i+4) + '.graphml'
            nx.write_graphml(G, filename)
            file = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\usedwords' + str(i+4) + '.txt'
            f = open(file, 'w+')
            f.write("%s" % '\n'.join(list(G.nodes)))
            f.close()        

    def dumpToFile(self):
        for i in range(4,8):
            G = self.load_graph(i)
            paths = dict(nx.all_pairs_shortest_path(G, 6))
            file = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\paths' + str(i) + '.json'
            with open(file, 'w+') as json_file:
                json.dump(paths, json_file)

    def load_graph(self, wordchars):
        file = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\graphs_' + str(wordchars) + '.graphml'
        graph = nx.read_graphml(file)
        return graph

    def getWords(self, wordchars):
        file = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\usedwords' + str(wordchars) + '.txt'
        with open(file) as file:
            dictionary = file.read().split()
        return dictionary
    
    def getPaths(self, wordchars):
        file = 'C:\\Workarea\\GitHub\\WordPuzzleGenerator\\wordpuzzle\\data\\graphs\\paths' + str(wordchars) + '.json'
        with open(file) as f:
            data = json.load(f)
        return data
        
    def changeLevel(self, level):
        self.level = level
        self.wordchars = LEVELS.get(level)
        self.graph = self.load_graph(self.wordchars)
        self.wordslist = self.getWords(self.wordchars)
        self.paths = self.getPaths(self.wordchars)
        self.start = None
        self.end = None
        self.currentpath = []
        self.currentstate = None
    
    def selectSourceTargetWords(self):
        found = False
        while not found:
            start = random.choice(self.wordslist)
            end = random.choice(self.wordslist)
            if nx.has_path(self.graph, start, end) == True:
                if nx.shortest_path_length(self.graph, start, end) <= 6:
                    self.start = start
                    self.end = end
                    self.currentstate = start
                    found = True
                    self.currentpath = self.paths[start][end]
                    print(self.paths[start][end])
            
    def checkInput(self, word):
        d = enchant.Dict('en_IE')
        found = False
        isLast = False
        if d.check(word):
            if word in self.currentpath:
                current = self.currentpath.index(self.currentstate)
                newword = self.currentpath.index(word)
                if newword - 1 == current:
                    self.currentstate = word
                    found = True
                    if newword + 1 == len(self.currentpath) - 1:
                        isLast = True
        return found, isLast