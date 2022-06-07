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
import sqlite3
import pygame_menu

conn = sqlite3.connect('LastGames.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Games (Player TEXT)")
conn.commit()

Tk().wm_withdraw()
pygame.init()

swidth = 1450
sheight = 900

screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('Monopoly')

font = pygame.font.SysFont('Times New Roman', 70)

bg_color = '#26272c'

ls = []
ls_with_colors = ['coral1', 'royalblue', 'seagreen1', 'tan1']





def draw_text(text, text_col, x, y, font): # Отрисовка текста
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def normalize(color): # Нормализация цвета
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

    def buy_field(self, id): # Покупка поля
        self.player_id = id
        self.color = ls_with_colors[self.player_id]
        self.price += 500

    def draw(self, img): # Отрисовка поля
        pygame.draw.rect(screen, normalize(self.color), (self.count_x-10, self.count_y-10, 120, 70), )
        #draw_text(str(self.price), 'black', self.count_x, self.count_y+70, font=pygame.font.SysFont('Times New Roman', 20))
        screen.blit(img, (self.count_x, self.count_y))

    def __repr__(self):
        return self.name


ls_company = []
with open('c.txt', 'r', encoding='utf-8') as f: # Компании берутся из файла c.txt
    for i in f.readlines():
        i = i.split()
        ls_company.append((i[0], i[1]))

dt_company = {i: k for i, k in ls_company}

ls_img = []
for s, k in enumerate(ls_company):
    if k[0] in {'start', 'police', 'question', 'lotery', 'nalog', 'jail'}:
        k = k[0] + '.png'
    else:
        k = k[0] + '.svg'

    img = pygame.transform.scale(pygame.image.load(f'map_svg/{k}'), (100, 50))
    ls_img.append(img)


class Field:
    def __init__(self):
        pass

    def draw_field(self, dt): # Рисуем поле игры
        count_x = 0
        count_y = 0

        for i, k in enumerate(ls_company, 1):
            k = k[0]
            if len(ls_comps) < len(ls_company):
                comp = Company(i, k.replace('.png', '').replace('.svg', ''), count_x, count_y, dt[k.replace('.png', '').replace('.svg', '')])
                comp.draw(img)
                ls_comps.append(comp)
                ls.append((count_x, count_y))
            else:

                for n, comp in enumerate(ls_comps, 0):
                    comp.draw(ls_img[n])

            if i > 0 and i <= 10:
                count_x += 130

            if i > 10 and i <= 20:
                count_y += 80

            if i > 20 and i <= 30:
                count_x -= 130

            if i > 30 and i <= 44:
                count_y -= 80


class Player:
    def __init__(self, id, name):
        self.name = name
        self.pos = 0
        self.id = id
        self.color = ls_with_colors[self.id]
        self.balance = 10000
        self.my_comps = []
        self.total_balance = self.get_balance()
        self.is_alive = True
        self.but = None
        self.but2 = None

    def get_balance(self): # total balance игрока
        self.total_balance = self.balance + sum(s.price for s in self.my_comps if len(self.my_comps) > 0)
        return self.total_balance

    def dice(self): # Бросить кубики
        global gln
        dice_num = random.randint(1, 6)
        dice_num2 = random.randint(1, 6)
        gln = (str(dice_num)+':'+str(dice_num2), self.color)

        return dice_num + dice_num2

    def move(self, num):

        if self.pos+num == len(ls_comps):
            self.pos = 0
        elif self.pos+num > len(ls_comps):
            self.pos = num - (len(ls_comps)-self.pos)
        else:
            self.pos += num

        pygame.display.update()

    def draw(self):
        if self.is_alive:
            pygame.draw.circle(screen, color=normalize(self.color), radius=20, center=(ls[self.pos][0]+25+self.id*3, ls[self.pos][1]+25+self.id*3))
            draw_text(f'{self.name}:{self.balance}/{self.total_balance}', self.color, 220, self.id*100+100, font=pygame.font.SysFont('Times New Roman', 50))

    def buy(self): # Покупка поля
        if ls_comps[self.pos].name.capitalize() in {'Start', 'Police', 'Question', 'Jail', 'Nalog'}:
            self.but.hide()
            return

        if ls_comps[self.pos].player_id == -1:
            if self.balance >= ls_comps[self.pos].price:
                self.balance -= ls_comps[self.pos].price
                ls_comps[self.pos].buy_field(self.id)
                self.my_comps.append(ls_comps[self.pos])
                self.get_balance()
                print(f'{self.color} Купил {ls_comps[self.pos]}')
            else:
                print('Недостаточно средств')
        else:
            if self.balance >= ls_comps[self.pos].price:
                self.balance -= ls_comps[self.pos].price
                ls_players[ls_comps[self.pos].player_id].balance += ls_comps[self.pos].price
                self.get_balance()
            else:
                print('Недостаточно средств')

            print(f'Рента {ls_comps[self.pos].price}')
        self.but.hide()
        pygame.display.update()

    def trade(self):
        def choice_player(player):
            print(player)
            menu2.disable()
            self.but2.hide()

        menu2 = pygame_menu.Menu('Обмен', swidth, sheight, theme=pygame_menu.themes.THEME_DARK)
        for p in ls_players:
            if p.id != self.id:
                menu2.add.button(f'{p.name}', lambda p=p: choice_player(p.name))
        menu2.mainloop(screen)

    def buy_request(self): # Добавление кнопки покупки
        cell = self.pos

        self.but2 = Button(screen, 530, 510, 250, 70, text=f'Обмен',
                      inactiveColour=normalize(self.color), radius=10,
                      onClick=lambda: self.trade(),
                      font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')

        if ls_comps[cell].name not in {'Start', 'Police', 'Question', 'Jail', 'Nalog', 'Lotery'}:

            if ls_comps[cell].player_id == -1:
                self.but = Button(screen, 680, 710, 300, 70, text=f'Купить {ls_comps[cell]} за {ls_comps[cell].price}',
                                  inactiveColour=normalize(self.color), radius=10,
                                  onClick=lambda: self.buy(),
                                  font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')

            else:
                self.but = Button(screen, 730, 710, 250, 70, text=f'Залпатить ренту {ls_comps[cell].price}',
                                  inactiveColour=normalize(self.color), radius=10,
                                  onClick=lambda: self.buy(),
                                  font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')
        else:
            if ls_comps[cell].name == 'Nalog':
                self.balance=-1000
                self.get_balance()
            elif ls_comps[cell].name == 'Police':
                pass
            elif ls_comps[cell].name == 'Question':
                pass
        pygame.display.update()



id_turn = 0
ls_lose = []


def start_(id):
    global id_turn
    player = ls_players[id]
    if player.is_alive:
        if player.total_balance > min([i.price for i in ls_comps]):
            num = player.dice()
            player.move(num)
            player.buy_request()



            player.total_balance -= 200
            if player.total_balance < min([i.price for i in ls_comps]):
                ls_players[id].is_alive = False
                ls_lose.append(player)
                id_turn += 1

            if id != 0:
                if ls_players[id-1].but != None:
                    ls_players[id-1].but.hide()
                    ls_players[id - 1].but2.hide()
            else:
                if ls_players[len(ls_players) - 1].but != None:
                    ls_players[len(ls_players)-1].but.hide()
                    ls_players[len(ls_players)-1].but2.hide()
            id_turn += 1
        else:
            ls_players[id].is_alive = False

    else:
        ls_lose.append(player)
        id_turn += 1

    if id_turn > len(ls_players) - 1:
        id_turn = 0

    pygame.display.update()


def main():
    global ls_players
    ls_players = [Player(i, str(i)) for i in range(sliderr.get_value())]

    f = Field()

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        screen.fill(bg_color)
        f.draw_field(dt_company)
        pygame.draw.rect(screen, normalize((224, 255, 255)), [200, 100, 300, 100*len(ls_players)])
        draw_text(gln[0], gln[1], 1000, 705, font=pygame.font.SysFont('Times New Roman', 70))

        for i in ls_players:
            i.draw()

        if len(ls_players) - len(ls_lose) == 1:
            print(ls_players[id_turn].name, 'Победил')
            draw_text(f'{ls_players[id_turn].name} Победил', 'pink', 500, 100, font)
            cursor.execute("INSERT INTO Games VALUES (?)", (ls_players[id_turn].name, ))
            conn.commit()


            run = False


            #run = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        butn = Button(screen, 1111, 710, 170, 70, text='Сделать ход', inactiveColour=ls_players[id_turn].color,
            hoverColour=normalize(ls_players[id_turn].color),
            pressedColour=normalize(ls_players[id_turn].color),
            onClick=lambda: start_(id_turn),
            font=pygame.font.SysFont('Times New Roman', 20), textVAlign='center')

        pw.update(events)

        pygame.display.update()
        pygame.display.flip()


def start_the_game():
    print('Hello', sliderr.get_value())
    main()
    menu.disable()


menu = pygame_menu.Menu('Welcome', swidth, sheight, theme=pygame_menu.themes.THEME_DARK)
sliderr = menu.add.range_slider('Количество игроков', default=2, range_values=[2, 3, 4])
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
