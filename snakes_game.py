import pygame
import numpy as np
import pandas as pd
import tkinter as tk
import math
import random
from tkinter import messagebox

class snake_body(object):
    rows = 40
    w = 1000
    def __init__(self,start, dirx=1,diry=0, color=(255,0,0)):
        self.position = start
        self.dirx = 1
        self.diry = 0
        self.color = color


    def moveBody(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.position = (self.position[0] + self.dirx, self.position[1] + self.diry)




    def drawBody(self,surface, eyes=False):
        dist = self.w // self.rows
        i = self.position[0]
        j = self.position[1]
        pygame.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2 ))
        if eyes:
            center = dist // 2
            radius = 3
            circleMiddle = (i*dist+center-radius, j*dist+8)
            circleMiddle2 = (i+dist + dist - radius*2, j*dist+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, position):
        self.color = color
        self.head = snake_body(position)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
    def moveSnake(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.position[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.position[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.position[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.position[:]] = [self.dirx, self.diry]

        for i,sb in enumerate(self.body):
            p = sb.position[:]
            if p in self.turns:
                turn = self.turns[p]
                sb.moveBody(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if sb.dirx == -1 and sb.position[0] <= 0: sb.position = (sb.rows-1, sb.position[1])
                elif sb.dirx == 1 and sb.position[0] >= sb.rows-1: sb.position = (0, sb.position[1])
                elif sb.diry == 1 and sb.position[1] >= sb.rows-1: sb.position = (sb.position[0], 0)
                elif sb.diry == -1 and sb.position[1] <= 0: sb.position = (sb.position[0], sb.rows-1)
                else: sb.moveBody(sb.dirx, sb.diry)




    def drawSnake(self, surface):
        for i, sb in enumerate(self.body):
            if i == 0:
                sb.drawBody(surface, True)
            else:
                sb.drawBody(surface)


    def addFood(self):
        tail = self.body[-1]
        dx = tail.dirx
        dy = tail.diry
        if dx == 1 and dy == 0:
            self.body.append(snake_body((tail.position[0]-1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(snake_body((tail.position[0]+1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(snake_body((tail.position[0], tail.position[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(snake_body((tail.position[0], tail.position[1]+1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy




    def reset(self, position):
        self.head = snake_body(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

def drawGrid(w, rows, surface):
    size = w // rows
    x = 0
    y = 0
    for line in range(rows):
        x = x + size
        y = y + size

        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y))


def drawWindow(surface):
    global rows,width, s, snack
    surface.fill((0,0,0))
    s.drawSnake(surface)
    snack.drawBody(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()



def randomSnack(rows, item):

    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.position == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)


def displayMessage(sub, cont):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(sub,cont)
    try:
        root.destroy()
    except:
        pass

def main():
    global rows, width, s, snack
    width = 1000
    rows = 40
    game_window = pygame.display.set_mode((width, width))
    s = snake((0,255,0), (20,20))
    snack = snake_body(randomSnack(rows,s), color=(0,255,0))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.moveSnake()
        if s.body[0].position == snack.position:
            s.addFood()
            snack = snake_body(randomSnack(rows,s), color=(0,255,0))
        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position, s.body[x+1:])):
                print('Score: ',len(s.body))
                displayMessage('Game Over !', 'Play again...')
                s.reset((20,20))
                break

        drawWindow(game_window)

    pass



main()
