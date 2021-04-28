import networkx as nx
import random
import enchant
import ujson
import os
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
        self.dir_path = self.getCurrentPath()
        self.wordslist = self.getWords(self.wordchars)
        self.paths = self.getPaths(self.wordchars)
        self.start = None
        self.end = None
        self.depth = None
        self.wordcount = None
        self.currentstate = None
        
    def getCurrentPath(self):
        script_dir = os.path.dirname(__file__)
        dirs = script_dir.split('\\')
        return '/'.join(dirs[:len(dirs)-1])

    def read_words_file(self):
        d = enchant.Dict('en_IE')
        rel_path = 'data/graphs/allwords.txt'
        abs_file_path = os.path.join(self.dir_path, rel_path)
        
        with open(abs_file_path, 'r') as file:
            dictionary = set(file.read().split())
            words = defaultdict(list)
            
            for i in range(4):
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
                        
            # Writing the graph to file
            rel_path = 'data/graphs/graphs_' + str(i+4) + '.graphml'
            abs_file_path = os.path.join(self.dir_path, rel_path)
            nx.write_graphml(G, abs_file_path)
            
    def load_graph(self, wordchars):
        rel_path = 'data/graphs/graphs_' + str(wordchars) + '.graphml'
        abs_file_path = os.path.join(self.dir_path, rel_path)
        graph = nx.read_graphml(abs_file_path)
        return graph    
    
    def dumpToFile(self):    
        for i in range(4,8):
            G = self.load_graph(i)
            paths = dict(nx.all_pairs_shortest_path(G, 6))
            output = []

            for word in paths:
                for path in list(paths[word]):
                    length = len(paths[word][path])
                    if length <= 1:
                        del paths[word][path]
                    if word not in output:
                        output.append(word)
            for word in list(paths):
                for path in list(paths[word]):
                    if bool(paths[word][path]) == False:
                        del paths[word][path]
                if bool(paths[word]) == False:
                    del paths[word]

            rel_path = 'data/graphs/paths' + str(i) + '.json'
            abs_file_path = os.path.join(self.dir_path, rel_path)
            with open(abs_file_path, 'w') as f:
                ujson.dump(paths, f)
            
            rel_path = 'data/graphs/usedwords' + str(i) + '.txt'
            abs_file_path = os.path.join(self.dir_path, rel_path)
            f = open(abs_file_path, 'w+')
            f.write("%s" % '\n'.join(list(output)))
            f.close()


    def getWords(self, wordchars):
        rel_path = 'data/graphs/usedwords' + str(wordchars) + '.txt'
        abs_file_path = os.path.join(self.dir_path, rel_path)
        with open(abs_file_path, 'r') as f:
            return f.read().split()
            
    def getPaths(self, wordchars):
        rel_path = 'data/graphs/paths' + str(wordchars) + '.json'
        abs_file_path = os.path.join(self.dir_path, rel_path)
        return ujson.load(open(abs_file_path))

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
            if end in self.paths[start]:
                length = len(self.paths[start][end])
                if length <= 7 and length > 3:
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
            if (word in self.paths[self.currentstate][word] and 
                len(self.paths[self.currentstate][word])) == 2:
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
    
    def reset(self):
        self.currentstate = self.start
        self.wordcount = 1
    
    def getNextWord(self):
        try:
            self.paths[self.currentstate][self.end]
        except KeyError:
            return None
        else:
            paths = self.paths[self.currentstate][self.end]
            return paths[1]
        
    def checkPath(self, wordsdict):
        for word, nextword in zip(wordsdict, wordsdict[1:]):
            try:
                self.paths[word][nextword]
            except KeyError:
                return False
            else:
                if nextword == self.end:
                    return True
        
    def getSolWord(self, word):
        d = enchant.Dict('en_IE')
        if d.check(word) and check(word):
            paths = self.paths[self.currentstate][word]
            self.wordcount += 1
            self.currentstate = paths[1]
            return paths[1]
            
    def getPath(self):
        return self.paths[self.start][self.end]