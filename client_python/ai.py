#!/usr/bin/env python
import random

class AI(object):
    def __init__(self, row, col, player):
        self.name   = "Guest" # CHANGEME
        self.row  = row
        self.col = col
        self.map  = [[0 for i in xrange(col)] for j in xrange(row)]
        self.player  = player

    def think(self):
        #
        # Your code here.
        # 
        # List of actions
        # - hesitate()  : do nothing
        # - put(row_num)    : put your block on selected row which is bounded by 0 ~ 15.
        # - chance(row1, row2) : you can use each one chance, do 2 put operations. You have totally 2 chances, and cannot use it sequentially.
        select = random.randrange(0,16)
        return self.put(select)

    def update(self, mapinfo):
        xpos, ypos = -1, 0
        for cell in mapinfo:
            xpos = xpos + 1
            if xpos == self.row:
                xpos = 0
                ypos = ypos + 1
            self.map[ypos][xpos] = int(cell)

    def hesitate(self):
        return "PASS\n"

    def put(self, select_row):
        return "PUT %d\n" % (select_row)
    
    def chance(self, select_row1, select_row2):
        return "CHANCE %d %d\n" %(select_row1, select_row2)

