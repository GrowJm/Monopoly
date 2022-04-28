import pygame
from pygame.locals import *
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button
from tkinter import Tk
from tkinter import messagebox
import random
from threading import Thread

Tk().wm_withdraw()
pygame.init()

swidth = 1000
sheight = 900

screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('Monopoly')

font = pygame.font.SysFont('Times New Roman', 20)

bg_color = '#26272c'

ls = []

def draw_text(text, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def normalize(color: str): #Нормализация цвета (из Color в RGB и наоборот)
    return pygame.Color(color)


class Company:
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var.keys()[0]

class Field:
    def __init__(self):
        pass

    def draw_field(self, dt):
        count_x = 0
        count_y = 0
        z = True

        for i, k in enumerate(dt, 1):
            img = pygame.transform.rotate(angle=90, surface=font.render(f'{k.replace(";", " ")}', True, normalize('black'), normalize('white')))
            screen.blit(img, (count_x, count_y))
            ls.append((count_x, count_y))
            if z is True:
                count_x += 130

            if i >= 7 and i <= 14:
                z = False
                count_y += 100

            if i > 14 and i <= 21:
                z = False
                count_x -= 130

            if i > 21 and i <= 28:
                z = False
                count_y -= 100


class Player:
    ls_with_colors = ['red', 'blue', 'green', 'yellow']

    def __init__(self, id):
        self.pos = 0
        self.id = id

    def dice(self):
        dice_num = random.randint(1, 6)
        dice_num2 = random.randint(1, 6)



        return dice_num + dice_num2

    def move(self, num):
        self.pos += num
        if self.pos > len(ls):
            self.pos = 0

    def draw(self):
        pygame.draw.circle(screen, color=normalize(self.ls_with_colors[self.id]), radius=10, center=ls[self.pos])


ls_players = [Player(i) for i in range(2)]
ls_company = []
ls_random = ['?', 'Лотерея', 'Полиция']

with open('c.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        i = i.split()
        ls_company.append((i[0], i[1]))
    ls_company.insert(0, ('Старт', 'Start'))

    for i in ls_random:
        ls_company.insert(random.randint(1, len(ls_company)-1), (i, 'Spec'))

dt_company = {i: k for i, k in ls_company}

id_turn = 0
def start_(id):
    global id_turn
    num = ls_players[id].dice()
    ls_players[id].move(num)
    id_turn += 1
    if id_turn > len(ls_players) - 1:
        id_turn = 0


f = Field()
run = True

while run:
    screen.fill(bg_color)
    f.draw_field(dt_company)
    for i in ls_players:
        i.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    Button(screen, 590, 490, 170, 70, text='Сделать ход', inactiveColour=normalize('violet'), radius=5, onClick=lambda: start_(id_turn),
        font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')

    pw.update(pygame.event.get())
    pygame.display.update()
    pygame.display.flip()

