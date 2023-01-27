import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


rect(screen, (196, 196, 196), (0, 0, 400, 400))     # Задний фон
circle(screen, (0, 0, 0), (200, 200), 102)          # Смайлик
circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (255, 0, 0), (150, 180), 20)         # Левый глаз
circle(screen, (0, 0, 0), (150, 180), 10)
circle(screen, (255, 0, 0), (250, 180), 18)         # Правый глаз
circle(screen, (0, 0, 0), (250, 180), 9)
polygon(screen, (0, 0, 0), [(100,130), (110,125),   # Левая бровь
                            (190,170), (180,175), (100,130)])
polygon(screen, (0, 0, 0), [(300,130), (290,125),   # Правая бровь
                            (210,170), (220,175), (300,130)])
rect(screen, (0, 0, 0), (150, 250, 100, 20))        # Рот
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
