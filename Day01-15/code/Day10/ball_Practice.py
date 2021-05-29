from abc import ABCMeta, abstractmethod
from enum import Enum, unique
from math import sqrt
from random import randint

import pygame


@unique
class Color(Enum):

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

@unique
class Direction(Enum):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Ball(object, metaclass=ABCMeta):

    def __init__(self, x, y, radius, sx, sy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True

    @abstractmethod
    def move(self, screen):
        pass

    def eat(self, other):
        if self.alive and other.alive and self != other:
            dx = self.x - other.x
            dy = self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance < self.radius + other.radius and self.radius > other.radius:
                other.alive = False
                self.radius = self.radius + int(other.radius * 0.146)

    @abstractmethod
    def draw(self, screen):
        pass

class Enemy(Ball):
    def __init__(self, x, y, radius, sx, sy, color):
        super().__init__(x, y, radius, sx, sy, color)

    def move(self,screen):
        self.x += self.sx
        self.y += self.sy
        if self.x - self.radius <= 0 or self.x + self.radius >= screen.get_width():
            self.sx = -self.sx
        if self.y - self.radius <= 0 or self.y + self.radius >= screen.get_height():
            self.sy = -self.sy

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class Player(Ball):
    def __init__(self, x, y, radius, sx, sy, color):
        super().__init__(x, y, radius, sx, sy, color)
        self.dir = Direction.LEFT
        print(self.color)

    def change_dir(self, new_dir):
        self.dir = new_dir

    def move(self,screen):
        amount = 10
        if self.dir == Direction.UP:
            self.y -= amount
        elif self.dir == Direction.RIGHT:
            self.x += amount
        elif self.dir == Direction.DOWN:
            self.y += amount
        else:
            self.x -= amount
        if self.x <= self.radius:
            self.x = self.radius
        elif self.x + self.radius >= screen.get_width():
            self.x = screen.get_width()-self.radius
        if self.y <= self.radius:
            self.y = self.radius
        elif self.y + self.radius >= screen.get_height():
            self.y = screen.get_height()-self.radius

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


def main():

    def handle_key_event(key_event):
        key = key_event.key
        if key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT):
            if player.alive:
                if key == pygame.K_UP:
                    new_dir = Direction.UP
                elif key == pygame.K_RIGHT:
                    new_dir = Direction.RIGHT
                elif key == pygame.K_DOWN:
                    new_dir = Direction.DOWN
                else:
                    new_dir = Direction.LEFT
                player.change_dir(new_dir)

    balls=[]
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('大球吃小球升级版')
    x, y = 400, 300
    running = True
    pcolor = Color.random_color()
    player = Player(x, y, 50, 0, 0, pcolor)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                handle_key_event(event)
        screen.fill((255, 255, 255))
        if pygame.time.get_ticks() % 50 == 0:
            x, y = randint(100, 500), randint(100, 700)
            radius = randint(10, 50)
            sx, sy = randint(-10, 10), randint(-10, 10)
            color = Color.random_color()
            ball = Enemy(x, y, radius, sx, sy, color)
            balls.append(ball)
        player.draw(screen)
        for ball in balls:
            if ball.alive:
                ball.draw(screen)
            else:
                balls.remove(ball)
        pygame.display.flip()
        pygame.time.delay(50)
        balls.append(player)
        for ball in balls:
            ball.move(screen)
            for other in balls:
                ball.eat(other)
        balls.remove(player)
        if player.alive == False:
            running = False



if __name__=='__main__':
    main()
