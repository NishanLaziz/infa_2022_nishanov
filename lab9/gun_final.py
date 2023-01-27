import math
from random import choice, randint
import pygame
pygame.init()

FPS = 30                        # Количество кадров в секунду
                                # Цвета
RED = 0xFF0000
BLUE = 0x0000FF
GREEN = 0x00FF00
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

WIDTH = 1200                    # Длина окна
HEIGHT = 800                    # Ширина окна
target_quantity = 10            # Количество шариков-мишеней


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        ''' Класс отвечает за шарики
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        '''
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10             # Радиус снаряда
        self.vx = 0
        self.vy = 0
        self.color = BLACK      # Цвет снаряда
        self.g = 1              # Ускорение свободного падения
        self.time = 0

    def move(self):
        ''' Движение снаряда с учетом гравитации и стен '''
        self.x += self.vx
        self.y -= self.vy
        self.time += 1
        self.vy -= self.g
        if self.y+self.r >= HEIGHT-50 and self.vy < 0:
            self.vy = -0.8 * self.vy
            self.vy -= self.g
            self.vx = 0.5 * self.vx
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx

    def draw(self):
        ''' Отрисовывает шарики '''
        pygame.draw.circle(self.screen, self.color,
                           (self.x, self.y), self.r)

    def hittest(self, obj):
        ''' Проверяет столкновение обьекта с целью, описываемой в обьекте obj.
            True - сталкиваются, False - нет
        obj - обьект, с которым проверяется столкновение.
        '''
        if math.sqrt((self.x-obj.x) ** 2 +
                     (self.y-obj.y) ** 2) <= self.r+obj.r:
            if type(obj) != Gun:
                return True
            elif self.time > 3:
                return True
        else:
            return False


class Shot:
    def __init__(self, screen, x, y):
        ''' Класс отвечает за снаряды
        x - начальное положение снаряда по горизонтали
        y - начальное положение снаряда по вертикали
        '''
        self.b = [Ball(screen, x, y)
                  for i in range(3)]

    def draw(self):
        ''' Отрисовывает снаряды '''
        for ball in self.b:
            ball.draw()


class Gun:
    def __init__(self, screen):
        ''' Класс отвечает за танк '''
        self.screen = screen
        self.f2_power = 30      # Сила выстрела снаряда
        self.f2_on = 0          # Стреляет ли пушка (1-да, 0-нет)
        self.an = 0             # Угол поворота пушки
        self.color = BLACK      # Цвет пушки
        self.x = 20             # Начальное положение танка по оси x
        self.y = 450            # Начальное положение танка по оси y
        self.angle = 0          # Угол поворота танка
        self.r = 15             # Размер танка для учета столкновений
        self.shot_type = 1      # Тип снаряда

    def fire2_start(self):
        ''' Заряжает пушку танка '''
        self.f2_on = 1
        self.f2_power = 30

    def fire2_end(self, event):
        ''' Выстрел мячом при отпускании кнопки мыши.
            Начальная скорость зависит от положения мыши. '''
        global balls, bullet, shots
        self.an = -math.atan2((event.pos[1] - self.y),
                              (event.pos[0] - self.x))
        bullet += 1
        if self.shot_type == 1:
            new_ball = Ball(self.screen, self.x, self.y)
            new_ball.r += 5
            new_ball.vx = 0.5 * self.f2_power * math.cos(-self.an)
            new_ball.vy = - 0.5 * self.f2_power * math.sin(-self.an)
            balls.append(new_ball)
        else:
            new_shot = Shot(self.screen, self.x, self.y)
            for i in range(3):
                new_shot.b[i].vx = 0.5 * self.f2_power * math.cos(- self.an + (i-1) * math.pi / 180 * 9)
                new_shot.b[i].vy = - 0.5 * self.f2_power * math.sin(- self.an + (i-1) * math.pi / 180 * 9)
            shots.append(new_shot)
        self.f2_on = 0
        self.f2_power = 30

    def targetting(self, event):
        ''' Режим прицеливания танка. Зависит от положения мыши. '''
        if event:
            self.an = - math.atan2((event.pos[1] - self.y),
                                   (event.pos[0] - self.x))

    def draw(self):
        ''' Отрисовывает танк с пушкой '''
        body = [(self.x - 20, self.y - 20),
                (self.x + 20, self.y - 20),
                (self.x + 20, self.y + 20),
                (self.x - 20, self.y + 20),
                (self.x - 20, self.y - 20)
                ]
        track1 = [(self.x - 25, self.y - 25),
                  (self.x + 25, self.y - 25),
                  (self.x + 25, self.y - 15),
                  (self.x - 25, self.y - 15)]

        track2 = [(self.x - 25, self.y + 25),
                  (self.x + 25, self.y + 25),
                  (self.x + 25, self.y + 15),
                  (self.x - 25, self.y + 15)]
        pygame.draw.polygon(self.screen, GREY,
                            rotate(body, self.x, self.y,
                                   self.angle), 0)
        pygame.draw.polygon(self.screen, BLACK,
                            rotate(track1, self.x, self.y,
                                   self.angle))
        pygame.draw.polygon(self.screen, BLACK,
                            rotate(track2, self.x, self.y,
                                   self.angle))
        pygame.draw.circle(self.screen, BLACK,
                           (self.x, self.y), 10, 0)
        pygame.draw.polygon(self.screen, self.color,
                            [(self.x - 5 * math.sin(self.an),
                              self.y - 5 * math.cos(self.an)),
                             (self.x + 5 * math.sin(self.an),
                              self.y + 5 * math.cos(self.an)),
                             (self.x + 5 * math.sin(self.an) +
                              self.f2_power * math.cos(self.an),
                              self.y + 5 * math.cos(self.an) -
                              self.f2_power * math.sin(self.an)),
                             (self.x - 5 * math.sin(self.an) +
                              self.f2_power * math.cos(self.an),
                              self.y - 5 * math.cos(self.an) -
                              self.f2_power * math.sin(self.an))]
                            )

    def shift(self, direction):
        ''' Описывает движения танка во время нажатия WASD
        direction - направление движения
        '''
        if direction == 'right':
            if self.angle != math.pi/4 and self.angle != -math.pi/4:
                self.x += 5
            else:
                self.x += 5 / math.sqrt(2)
        elif direction == 'left':
            if self.angle != math.pi/4 and self.angle != -math.pi/4:
                self.x -= 5
            else:
                self.x -= 5 / math.sqrt(2)
        elif direction == 'up':
            if self.angle != math.pi/4 and self.angle != -math.pi/4:
                self.y -= 5
            else:
                self.y -= 5 / math.sqrt(2)
        elif direction == 'down':
            if self.angle != math.pi/4 and self.angle != -math.pi/4:
                self.y += 5
            else:
                self.y += 5 / math.sqrt(2)

    def move(self, pressed):
        ''' Задает направление танка
        pressed - зажатая клавиша
        '''
        k = 0
        if pressed[pygame.K_d]:
            self.shift('right')
            k += 5
        elif pressed[pygame.K_a]:
            self.shift('left')
            k += 11
        if pressed[pygame.K_w]:
            self.shift('up')
            k += 16
        elif pressed[pygame.K_s]:
            self.shift('down')
            k += 20
        if k == 5 or k == 11:
            self.angle = 0
        elif k == 16 or k == 20:
            self.angle = math.pi / 2
        elif k == 21 or k == 31:
            self.angle = math.pi / 4
        elif k == 27 or k == 25:
            self.angle = -math.pi / 4

    def power_up(self):
        ''' Зарядка пушки танка '''
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = BLACK


class Target:
    def __init__(self, screen):
        ''' Класс отвечает за шарики-мишени '''
        self.points = 0         # Количество очков
        self.live = 1           # Жив ли шарик-мишень (1-да, 0-нет)
        self.screen = screen
        self.new_target()
        self.vy = randint(-7, 7)
        self.vx = randint(-7, 7)

    def new_target(self):
        ''' Создание нового шарика-мишени '''
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def hit(self):
        ''' Выдает очки за попадание в шарик-мишень '''
        self.points += 1

    def draw(self):
        ''' Отрисовывает шарик-мишень '''
        pygame.draw.circle(self.screen, self.color,
                           (self.x, self.y), self.r, 0)

    def move(self):
        ''' Движение шарика-мишени '''
        self.y += self.vy
        self.x += self.vx
        if self.y+self.r > HEIGHT or self.y-self.r < 0:
            self.vy = -self.vy
        if self.x+self.r > WIDTH or self.x-self.r < 0:
            self.vx = -self.vx

    def hittest(self, obj):
        ''' Проверяет столкновение обьекта с целью, описываемой в обьекте obj.
            True - сталкиваются, False - нет
        obj - обьект, с которым проверяется столкновение.
        '''
        if math.sqrt((self.x-obj.x) ** 2 +
                     (self.y-obj.y) ** 2) <= self.r+obj.r:
            return True
        else:
            return False


def display_text_c(screen, word, word_color, x, y, font_size):
    ''' Отображает текст в центре
    word - слово, которое надо отобразить
    word_color - цвет слова
    x, y - координаты центра текста
    font_size - размер текста
    '''
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    text = font.render(word, True, word_color)
    text_field = text.get_rect()
    text_field.center = (x, y)
    screen.blit(text, text_field)


def display_text_tl(screen, word, word_color, x, y, font_size):
    ''' Отображает текст слева сверху
    word - слово, которое надо отобразить
    word_color - цвет слова
    x, y - координаты верхнего левого угла текста
    font_size - размер текста
    '''
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    text = font.render(word, True, word_color)
    text_field = text.get_rect()
    text_field.topleft = (x, y)
    screen.blit(text, text_field)


def score_indicate(screen, score, bullet, font_size):
    ''' Отвечает за отображение счета на экране
    score - количество очков
    bullet -  количество выстрелов
    x, y - координаты верхнего левого угла текста
    font_size - размер шрифта
    '''
    display_text_tl(screen, 'Очков: ' + str(score), BLACK,
                    0, 0, font_size)
    display_text_tl(screen, 'Выстрелов: ' + str(bullet), BLACK,
                    0, 50, font_size)


def start_screen(screen):
    ''' Отображает экран с правилами в начале игры '''
    global finished
    screen.fill(WHITE)
    display_text_c(screen, 'Чтобы управлять танком, используйте WASD',
                   BLACK, WIDTH/2, HEIGHT/2 - 50, 50)
    display_text_c(screen, 'Сменить оружие можно нажатием 1 и 2',
                   BLACK, WIDTH/2, HEIGHT/2, 50)
    display_text_c(screen, 'Если мишени или ваши снаряды поразят танк, то игра завершится',
                   BLACK, WIDTH/2, HEIGHT/2 + 50, 50)
    pygame.display.update()
    pygame.time.wait(3000)


def end_screen(screen, score, bullet):
    ''' Отображает экран с результатми в конце игры
    score - количество очков
    bullet - количество выстрелов
    '''
    screen.fill(WHITE)
    display_text_c(screen, 'Игра окончена',
                   BLACK, WIDTH/2, HEIGHT/5, 150)
    display_text_c(screen, 'Очков: ' + str(score),
                   BLACK, WIDTH/2, HEIGHT/2 - 50, 100)
    display_text_c(screen, 'Выстрелов: ' + str(bullet),
                   BLACK, WIDTH/2, HEIGHT/2 + 50, 100)
    pygame.display.update()


def rotate(subject, x, y, angle):
    ''' Поворачивает объект вокруг точки и выдает новые координаты
    subject - объект
    x, y - координаты точки поворота
    angle - угол поворота
    '''
    z = [((subject[i][0] - x) * math.cos(angle) -
          (subject[i][1] - y) * math.sin(-angle) + x,
          (subject[i][1] - y) * math.cos(angle) +
          (subject[i][0] - x) * math.sin(-angle) + y)
         for i in range(len(subject))
         ]
    return z


def game_move(screen, balls, gun, target_set):
    global game_live
    ''' Передвигает шары, проверяет коллизии и убирает "стоячие" снаряды
    balls - массив с шарами
    gun - танк
    target_set - мишени
    '''
    i = 0
    while i < len(balls):
        balls[i].move()
        for target in target_set:
            if balls[i].hittest(target) and target.live:
                target.hit()
                target.new_target()
        if balls[i].hittest(gun):
            game_live = 0
        if abs(balls[i].vy) <= 3 and balls[i].y > HEIGHT - 70:
            balls.pop(i)
            i -= 1
        i += 1
    for target in target_set:
        if target.hittest(gun):
            game_live = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False
game_live = 1                   # Идет ли игра (1-да, 0-нет)
bullet = 0                      # Количество выстрелов
score = 0                       # Количество очков
balls = []                      # Массив шариков
shots = []                      # Массив снарядов
gun = Gun(screen)
target_set = [Target(screen)
              for i in range(target_quantity)]

#Начальный экран
start_screen(screen)

while not finished:
# Начальное отображение
    screen.fill(WHITE)
    gun.draw()
    score_indicate(screen, score, bullet, 50)
    for target in target_set:
        target.draw()
    for b in balls:
        b.draw()
    for shot in shots:
        shot.draw()
    pygame.display.update()
# Наведение и стрельба пушки танка
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            game_over = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
# Смена типа оружия танка
    pressed = pygame.key.get_pressed()
    gun.move(pressed)
    if pressed[pygame.K_1]:
        gun.shot_type = 1
    if pressed[pygame.K_2]:
        gun.shot_type = 2
# Движение снарядов и проверка проверка на попадание по мишени
    game_move(screen, balls, gun, target_set)
    i = 0
    while i < len(shots):
        game_move(screen, shots[i].b, gun, target_set)
        if shots[i].b[0].time > 30:
            shots.pop(i)
            i -= 1
        i += 1
# Проверка попадания по танку
    if game_live == 0:
        end_screen(screen, score, bullet)
        finished = True
        game_over = True
# Движение шариков-мишеней
    for target in target_set:
        target.move()
    gun.power_up()
# Подсчет очков
    score = 0
    for target in target_set:
        score += target.points

# Конец игры
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
            finished = True
        pygame.time.wait(20)

pygame.quit()
