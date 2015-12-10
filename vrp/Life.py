# -*- coding: utf-8 -*-

"""Life.py

生命类
"""

import random


class Life(object):
    env = None
    gene = ""
    score = 0
    separate_indexs = []
    distance = 0

    def __init__(self, env, gene=None):
        self.env = env

        if gene == None:
            # self.__rndGene()
            pass
        elif type(gene) == type([]):
            self.gene = []
            for k in gene:
                self.gene.append(k)
        else:
            self.gene = gene

    def __rndGene(self):
        self.gene = ""
        for i in range(self.env.geneLength):
            self.gene += str(random.randint(0, 1))

    def setScore(self, v):
        self.score = v

    def addScore(self, v):
        self.score += v

    def set_distance(self, v):
        self.distance = v
