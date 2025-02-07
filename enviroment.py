import pygame
class Enviroment:
    def __init__(self):
        self.display_screen = None

ENV = Enviroment()


class Block:
    def __init__(self, size=(50, 50), pos=(0, 0), color="white"):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.color = color

    def draw(self, screen,):
        pygame.draw.rect(screen, self.color, self.rect)


class Movable_Block(Block):
    def __init__(self, size=(50, 50), pos=(0, 0), color="white", velocity=(0, 0)):
        super().__init__(size, pos, color)
        self.velocity = velocity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        self.rect = pygame.Rect(self.pos, self.size)

counter = 0

