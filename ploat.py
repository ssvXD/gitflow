import pygame
import sys
import time
import os

import start_screen
from enviroment import ENV


def ploat(screen):
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Пиксельный Демон")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    frames = [
        pygame.image.load('demon1.png'),
        pygame.image.load('demon2.png'),
        pygame.image.load('demon3.png'),
        pygame.image.load('demon4.png')
    ]

    scale_factor = 4
    frames = [pygame.transform.scale(frame, (frame.get_width() * scale_factor, frame.get_height() * scale_factor)) for frame in frames]

    frame_count = len(frames)
    current_frame = 0
    animation_speed = 0.2

    font = pygame.font.Font(None, 36)

    class AnimatedDemon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.frames = frames
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 3))

        def update(self):
            self.current_frame += animation_speed
            if self.current_frame >= frame_count:
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]

    def draw_text(text, x, y, color=RED):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    demon = AnimatedDemon()

    clock = pygame.time.Clock()
    running = True
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            current_time = time.time()
            if current_time - start_time > 3:
                running = False
                ENV.display_screen = 0
                return

        demon.update()

        screen.fill(BLACK)

        screen.blit(demon.image, demon.rect)

        draw_text("Добро пожаловать в ад,", 390, 50)
        draw_text("Алекс!", 370, 355)
        draw_text("Ты открыл древнюю книгу,", 195, 400)
        draw_text("и теперь тебе предстоит пройти", 565, 400)
        draw_text("через темные уровни!", 390, 455)
        draw_text("Только смелые выживут!", 390, 500)

        pygame.display.flip()

        clock.tick(30)
