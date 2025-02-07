import pygame
import sys
import time
import os

import start_screen
from enviroment import ENV


def ploat(screen):
    # Инициализация Pygame
    pygame.init()

    # Настройки экрана
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Пиксельный Демон")

    # Цвета
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)  # Красный цвет для текста

    # Загрузка кадров анимации
    frames = [
        pygame.image.load('demon1.png'),  # Загрузите первый кадр
        pygame.image.load('demon2.png'),  # Загрузите второй кадр
        pygame.image.load('demon3.png'),  # Загрузите третий кадр
        pygame.image.load('demon4.png')   # Загрузите четвертый кадр
    ]

    # Масштабирование кадров в 4 раза
    scale_factor = 4
    frames = [pygame.transform.scale(frame, (frame.get_width() * scale_factor, frame.get_height() * scale_factor)) for frame in frames]

    # Параметры анимации
    frame_count = len(frames)  # Количество кадров
    current_frame = 0          # Текущий кадр
    animation_speed = 0.2      # Скорость смены кадров

    # Настройка шрифта
    font = pygame.font.Font(None, 36)

    class AnimatedDemon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()  # Вызываем конструктор родительского класса
            self.frames = frames  # Список кадров
            self.current_frame = 0
            self.image = self.frames[self.current_frame]  # Текущий кадр
            # Размещаем демона выше и по центру
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 3))

        def update(self):
            # Изменение кадра для "анимации"
            self.current_frame += animation_speed
            if self.current_frame >= frame_count:
                self.current_frame = 0  # Зацикливаем анимацию
            self.image = self.frames[int(self.current_frame)]  # Обновляем текущий кадр

    def draw_text(text, x, y, color=RED):  # Используем красный цвет для текста
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))  # Центрируем текст
        screen.blit(text_surface, text_rect)

    # Создание экземпляра демона
    demon = AnimatedDemon()

    # Главный игровой цикл
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

        # Обновление анимации демона
        demon.update()

        # Заливка фона
        screen.fill(BLACK)

        # Отображение анимированного демона
        screen.blit(demon.image, demon.rect)

        # Отображение текста от демона с эффектами
        draw_text("Добро пожаловать в ад,", 390, 50)
        draw_text("Алекс!", 370, 355)
        draw_text("Ты открыл древнюю книгу,", 195, 400)
        draw_text("и теперь тебе предстоит пройти", 565, 400)
        draw_text("через темные уровни!", 390, 455)
        draw_text("Только смелые выживут!", 390, 500)

        # Обновление экрана
        pygame.display.flip()

        # Установка частоты кадров (FPS)
        clock.tick(30)


