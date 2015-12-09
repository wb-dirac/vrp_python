# -*- coding: utf-8 -*-

"""TSP.py

TSP问题
"""

import sys
import random
import math
import time
import Tkinter
import threading
from GA import GA
from Life import Life

class MyTSP(object):
    "TSP"

    def __init__(self, root, width=800, height=600, n=100):
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.condition = 2000
        self.canvas = Tkinter.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#ffffff",
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
        self.title("TSP")
        self.__r = 5
        self.__t = None
        self.__lock = threading.RLock()

        self.__bindEvents()
        self.new()

    def __bindEvents(self):
        self.root.bind("q", self.quite)
        self.root.bind("n", self.new)
        self.root.bind("e", self.evolve)
        self.root.bind("s", self.stop)

    def title(self, s):
        self.root.title(s)

    def new(self, evt=None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()
        self.nodes = []  # 节点坐标
        self.nodes2 = []  # 节点图片对象
        x, y = self.width / 2, self.height / 2
        self.start = (x, y)
        self.canvas.create_oval(x - self.__r,
                                           y - self.__r, x + self.__r, y + self.__r,
                                           fill="#00ff00",
                                           outline="#000000",
                                           tags="O",
                                           )
        for i in range(self.n):
            x = random.random() * (self.width - 60) + 30
            y = random.random() * (self.height - 60) + 30
            self.nodes.append((x, y))
            node = self.canvas.create_oval(x - self.__r,
                                           y - self.__r, x + self.__r, y + self.__r,
                                           fill="#ff0000",
                                           outline="#000000",
                                           tags="node",
                                           )
            self.nodes2.append(node)

        self.ga = GA(
            lifeCount=50,
            mutationRate=0.05,
            judge=self.judge(),
            mkLife=self.mkLife(),
            xFunc=self.xFunc(),
            mFunc=self.mFunc(),
            save=self.save()
        )
        self.order = range(self.n)
        init_life = Life(self, self.order)
        jg = self.judge()
        jg(init_life)
        self.line(init_life)

    def distance(self, order):
        "得到当前顺序下连线总长度"
        distance = 0
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1, p2 = self.nodes[i1], self.nodes[i2]
            distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        return distance

    def mkLife(self):
        def f():
            lst = range(self.n)
            random.shuffle(lst)
            return lst

        return f

    def judge(self):
        "评估函数"
        def f(lf, av=100):
            lf.separate_indexs = []
            path = lf.gene
            path_len = len(lf.gene)  # 路径长度，不包括起点
            i = 0  # 路径中 node 的指针
            p1 = self.start
            total_distance = 0
            one_distance = 0
            while i < path_len:
                p2 = self.nodes[path[i]]
                distance = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
                if one_distance + distance > self.condition:
                    # 重置迭代变量
                    if p1 == self.start:
                        raise RuntimeError("point{}far from{}".format(p2, p1))
                    one_distance = 0
                    p1 = self.start
                    lf.separate_indexs.append(i)
                else:
                    p1 = p2
                    one_distance += distance
                    total_distance += distance
                    i += 1
            lf.set_distance(total_distance)
            lf.separate_indexs.append(i)
            return 1 / (len(lf.separate_indexs) * 1600 + total_distance)
        # return lambda lf, av=100: 1.0 / self.distance(lf.gene)
        return f
    def xFunc(self):
        "交叉函数"

        def f(lf1, lf2):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(self.n - 1, self.n)
            g1 = lf2.gene[p1:p2] + lf1.gene
            # g2 = lf1.gene[p1:p2] + lf2.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11

        return f

    def mFunc(self):
        "变异函数"

        def f(gene):
            p1 = random.randint(0, self.n - 2)
            p2 = random.randint(self.n - 2, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            return gene

        return f

    def save(self):
        def f(lf, gen):
            pass

        return f

    def evolve(self, evt=None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        while self.__running:
            self.ga.next()
            self.line(self.ga.best)
            self.title("TSP - gen: %d" % self.ga.generation)
            self.canvas.update()

        self.__t = None

    def line(self, life):
        order = life.gene
        "将节点按 order 顺序连线 以life.separete_indexs 分割"
        self.canvas.delete("line")

        def line2(i1, i2):
            p1 = self.start if i1 == -1 else self.nodes[i1]
            p2 = self.nodes[i2]
            self.canvas.create_line(p1, p2, fill="#000000", tags="line")
            return i2
        start_number = 0
        for i in life.separate_indexs:
            reduce(line2, order[start_number:i], -1)
            start_number = i

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        sys.exit()

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    MyTSP(Tkinter.Tk()).mainloop()
