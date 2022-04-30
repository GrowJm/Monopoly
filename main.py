import time
import asyncio
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

font = pygame.font.SysFont('Times New Roman', 70)

bg_color = '#26272c'

ls = []
ls_with_colors = ['coral1', 'royalblue', 'seagreen1', 'tan1']


def draw_text(text, text_col, x, y, font):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def normalize(color):
    return pygame.Color(color)


gln = (' ', normalize(bg_color))
ls_comps = []


class Company:
    def __init__(self, cell_id, name, count_x, count_y, group):
        self.player_id = -1
        self.color = 'white'
        self.price = random.choice([i for i in range(200, 2500, 500)])
        self.cell_id = cell_id
        self.name = name.replace('_', ' ').capitalize()
        self.count_x = count_x
        self.count_y = count_y
        self.group = group

    def buy_field(self, id):
        self.player_id = id
        self.color = ls_with_colors[self.player_id]
        self.price += 500
        #self.draw()

    def draw(self, img):
        #print(self.color)
        pygame.draw.rect(screen, normalize(self.color), (self.count_x-10, self.count_y-10, 70, 70), )
        screen.blit(img, (self.count_x, self.count_y))

    def __repr__(self):
        return self.name


ls_company = []
ls_random = ['question', 'lotery', 'police']
with open('c.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        i = i.split()
        ls_company.append((i[0], i[1]))
    ls_company.insert(0, ('start', 'Start'))

    for i in ls_random:
        ls_company.insert(random.randint(1, len(ls_company)-1), (i, 'Spec'))

dt_company = {i: k for i, k in ls_company}

ls_img = []
for k in dt_company:
    if k == 'start':
        k = 'start.png'
    elif k == 'police':
        k = 'police.png'
    elif k == 'question':
        k = 'question.png'
    elif k == 'lotery':
        k = 'lotery.png'
    else:
        k = k + '.svg'

    img = pygame.transform.rotate(angle=90, surface=pygame.transform.scale(pygame.image.load(f'map_svg/{k}'), (50, 50)))
    ls_img.append(img)

class Field:
    def __init__(self):
        pass

    def draw_field(self, dt):
        count_x = 0
        count_y = 0
        z = True

        for i, k in enumerate(dt, 1):
            if k == 'Старт':
                k = 'start.png'
            elif k == 'Полиция':
                k = 'police.png'
            elif k == '?':
                k = 'question.png'
            elif k == 'Лотерея':
                k = 'lotery.png'
            else:
                k = k+'.svg'

            if len(ls_comps) < len(dt):
                comp = Company(i, k.replace('.png', '').replace('.svg', ''), count_x, count_y, dt[k.replace('.png', '').replace('.svg', '')])
                comp.draw(img)
                ls_comps.append(comp)
                ls.append((count_x, count_y))
            else:

                for n, comp in enumerate(ls_comps, 0):
                    comp.draw(ls_img[n])

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
    def __init__(self, id, name):
        self.name = name
        self.pos = 0
        self.id = id
        self.color = ls_with_colors[self.id]
        self.balance = 5000
        self.my_comps = []
        self.total_balance = self.get_balance()
        self.is_alive = True

    def get_balance(self):
        self.total_balance = self.balance + sum(s.price for s in self.my_comps if len(self.my_comps) > 0)
        return self.total_balance

    def dice(self):
        global gln
        dice_num = random.randint(1, 6)
        dice_num2 = random.randint(1, 6)
        gln = (str(dice_num)+':'+str(dice_num2), self.color)

        return dice_num + dice_num2

    def move(self, num):
        if self.pos+num == 29:
            self.pos = 0
        if self.pos+num > len(ls_comps):
            self.pos = num - (len(ls_comps)-self.pos)
            #print(self.pos, num, len(ls_comps), self.color)
        else:
            self.pos += num

    def draw(self):
        if self.is_alive:
            pygame.draw.circle(screen, color=normalize(self.color), radius=10, center=(ls[self.pos][0]+25+self.id*3, ls[self.pos][1]+25+self.id*3))
            draw_text(f'{self.name}:{self.balance}/{self.total_balance}', self.color, 125, self.id*100+100, font = pygame.font.SysFont('Times New Roman', 50))

    def buy(self):
        if ls_comps[self.pos].name in {'Start', 'Police', 'Question'}:
            return

        if ls_comps[self.pos].player_id == -1:
            if self.balance >= ls_comps[self.pos].price:
                self.balance -= ls_comps[self.pos].price
                ls_comps[self.pos].buy_field(self.id)
                self.my_comps.append(ls_comps[self.pos])
                self.get_balance()
                print(f'{self.color} Купил {ls_comps[self.pos]}')
            else:
                messagebox.showinfo('!', 'Недостаточно средств')
        else:
            messagebox.showinfo('!', f'Игрок {ls_comps[self.pos].player_id} уже владеет этим полем')
        pygame.display.update()

    def buy_request(self):
        #print(ls_comps, self.pos, '------')
        cell = self.pos
        if cell == 29:
            cell = 0

        Button(screen, 300, 300, 250, 70, text=f'Купить {ls_comps[cell]}', inactiveColour=normalize(self.color), radius=5,
                onClick=lambda: self.buy(),
                font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')


ls_players = [Player(i, str(i)) for i in range(4)]

id_turn = 0


def start_(id):
    global id_turn
    num = ls_players[id].dice()
    ls_players[id].move(num)
    ls_players[id].buy_request()
    id_turn += 1
    if id_turn > len(ls_players) - 1:
        id_turn = 0


f = Field()

run = True

while run:
    screen.fill(bg_color)
    f.draw_field(dt_company)
    pygame.draw.rect(screen, normalize((224, 255, 255)), [100, 100, 300, 100*len(ls_players)])
    draw_text(gln[0], gln[1], 400, 480, font = pygame.font.SysFont('Times New Roman', 70))

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

