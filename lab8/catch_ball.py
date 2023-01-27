import pygame
from pygame.draw import *
from random import randint
import numpy as np
pygame.init()

# Константы
FPS = 100       # Количество кадров в секунду
width = 1200    # Длина экрана
height = 600    # Ширина экрана
R_max = 100     # Максимальный радиус шарика
R_min = 10      # Минимальный радиус шарика
n_max = 10      # Максимальное количество шаров на экране -1

# Переменные
n = 0           # Количество шариков на экране
score = 0       # Количество очков
hit = 0         # Количество попаданий
balls = np.zeros((n_max, 6))
'''
balls(x, y, r, color, speed, alpha)
x, y - координаты центра шарика
r - радиус шарика
color - цвет шарика
speed - скорость шарика
alpha - угол направления шарика
'''

screen = pygame.display.set_mode((width, height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball(balls, n):
    ''' Создает новый шарик
    balls - массив шариков
    n - количество шариков на экране +1
    '''
    balls[n,2] = randint(R_min, R_max)
    balls[n,0] = randint(balls[n,2], width-balls[n,2])
    balls[n,1] = randint(balls[n,2], height-balls[n,2])
    balls[n,3] = randint(0, 5)
    balls[n,4] = randint(1, 7)
    balls[n,5] = randint(0, 360)


def print_ball(balls):
    ''' Отображает шарики на экране
    balls - массив шариков
    '''
    for i in range(0, n_max):
        circle(screen, COLORS[int(balls[i,3])], (balls[i,0], balls[i,1]), balls[i,2])
    pygame.display.update()
    screen.fill(BLACK)


def click(event, balls):
    ''' Определяет количество попаданий мышкой
    event - событие нажатия мышкой
    balls - массив шариков
    '''
    hit = 0
    x_click, y_click = event.pos
    for i in range(0, n_max):
        if np.sqrt((balls[i,0]-x_click)**2 + (balls[i,1]-y_click)**2) < balls[i,2]:
            if i < n_max-1:
                for j in range(i, n_max-1):
                    balls[j] = balls[j+1]
            balls[n_max-1] = np.zeros(6)
            hit += 1
    return hit


def motion_ball(balls):
    ''' Описывает движение и столкновение шариков со стенкой
    balls - массив шариков
    '''
    beta = balls[:,5]
    for i in range(0, n_max):
        if (balls[i,0] + balls[i,2]) > width:
            beta[i] = 180 - balls[i,5]
        if (balls[i,1] + balls[i,2]) > height:
            beta[i] = 360 - balls[i,5]
        if (balls[i,0] - balls[i,2]) < 0:
            beta[i] = 180 - balls[i,5]
        if (balls[i,1] - balls[i,2]) < 0:
            beta[i] = 360 - balls[i,5]
    for i in range(0, n_max):
        balls[i,0] += int(balls[i,4] * np.cos(np.pi*beta[i]/180) * (FPS/100))
        balls[i,1] += int(balls[i,4] * np.sin(np.pi*beta[i]/180) * (FPS/100))
        balls[i,5] = beta[i]


def score_indicate(score):
    ''' Отвечает за отображение счета на экране
    score - количество очков
    '''
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render(str(score), False, (255, 255, 255))
    screen.blit(textsurface,(0,0))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

create_ball_event = pygame.USEREVENT
pygame.time.set_timer(create_ball_event, 1000)


while not finished:
    clock.tick(FPS)

# Проверка на количество одновременных шаров на экране
    if n == n_max:
        for i in range(0, n_max-1):
            balls[i] = balls[i+1]
        n -= 1

# Проверка нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hit = click(event, balls)
            if hit > 0:
                score += hit
                n -= hit
            hit = 0
            print_ball(balls)
        elif event.type == create_ball_event:
            new_ball(balls, n)
            n += 1
            print_ball(balls)

    motion_ball(balls)
    score_indicate(score)
    print_ball(balls)

pygame.quit()
