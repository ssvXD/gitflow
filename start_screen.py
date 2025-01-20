import pygame
import random
import time
import os
import sys
from level_1 import level_1


def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {filename}. Ошибка: {e}")
        sys.exit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)


    def draw(screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Welcome to hell!", True, (255, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))


    def pixiles(screen):
        for i in range(10000):
            screen.fill(pygame.Color('white'),
                        (random.random() * width,
                         random.random() * height, 1, 1))


    all_sprites = pygame.sprite.Group()

    # Кнопка первого уровня
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("level1-Photoroom.png")
    sprite.image = pygame.transform.scale(sprite.image, (100, 100))
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 0
    sprite.rect.y = 0
    all_sprites.add(sprite)

    # Кнопка второго уровня
    sprite2 = pygame.sprite.Sprite()
    sprite2.image = load_image("level2-Photoroom.png")
    sprite2.image = pygame.transform.scale(sprite2.image, (100, 100))
    sprite2.rect = sprite2.image.get_rect()
    sprite2.rect.x = sprite.rect.x + sprite.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite2.rect.y = 0
    all_sprites.add(sprite2)
    # Кнопка третьего уровня
    sprite3 = pygame.sprite.Sprite()
    sprite3.image = load_image("level3-Photoroom.png")
    sprite3.image = pygame.transform.scale(sprite3.image, (100, 100))
    sprite3.rect = sprite3.image.get_rect()
    sprite3.rect.x = sprite2.rect.x + sprite2.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite3.rect.y = 0
    all_sprites.add(sprite3)
    # Кнопка четвертого уровня
    sprite4 = pygame.sprite.Sprite()
    sprite4.image = load_image("level4-Photoroom.png")
    sprite4.image = pygame.transform.scale(sprite4.image, (100, 100))
    sprite4.rect = sprite4.image.get_rect()
    sprite4.rect.x = sprite3.rect.x + sprite3.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite4.rect.y = 0
    all_sprites.add(sprite4)
    # Кнопка пятого уровня
    sprite5 = pygame.sprite.Sprite()
    sprite5.image = load_image("level5-Photoroom.png")
    sprite5.image = pygame.transform.scale(sprite5.image, (100, 100))
    sprite5.rect = sprite5.image.get_rect()
    sprite5.rect.x = sprite4.rect.x + sprite4.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite5.rect.y = 0
    all_sprites.add(sprite5)
    # Кнопка шестого уровня
    sprite6 = pygame.sprite.Sprite()
    sprite6.image = load_image("level6-Photoroom.png")
    sprite6.image = pygame.transform.scale(sprite6.image, (100, 100))
    sprite6.rect = sprite6.image.get_rect()
    sprite6.rect.x = sprite5.rect.x + sprite5.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite6.rect.y = 0
    all_sprites.add(sprite6)
    # Кнопка седьмого уровня
    sprite7 = pygame.sprite.Sprite()
    sprite7.image = load_image("level7-Photoroom.png")
    sprite7.image = pygame.transform.scale(sprite7.image, (100, 100))
    sprite7.rect = sprite7.image.get_rect()
    sprite7.rect.x = sprite6.rect.x + sprite6.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite7.rect.y = 0
    all_sprites.add(sprite7)
    # Кнопка восьмого уровня
    sprite8 = pygame.sprite.Sprite()
    sprite8.image = load_image("level8-Photoroom.png")
    sprite8.image = pygame.transform.scale(sprite8.image, (100, 100))
    sprite8.rect = sprite8.image.get_rect()
    sprite8.rect.x = sprite7.rect.x + sprite7.rect.width + 2  # Отступ в 10 пикселей между спрайтами
    sprite8.rect.y = 0
    all_sprites.add(sprite8)



    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if sprite.rect.collidepoint(mouse_pos):
                    # Вход в 1 уровень
                    print("сасиски1")
                    level_1()
                elif sprite2.rect.collidepoint(mouse_pos):
                    # Вход во 2 уровень
                    print("сасиски2")
                elif sprite3.rect.collidepoint(mouse_pos):
                    # Вход в 3 уровень
                    print("сасиски3")
                elif sprite4.rect.collidepoint(mouse_pos):
                    # Вход в 4 уровень
                    print("сасиски4")
                elif sprite5.rect.collidepoint(mouse_pos):
                    # Вход в 5 уровень
                    print("сасиски5")
                elif sprite6.rect.collidepoint(mouse_pos):
                    # Вход в 6 уровень
                    print("сасиски6")
                elif sprite7.rect.collidepoint(mouse_pos):
                    # Вход в 7 уровень
                    print("сасиски7")
                elif sprite8.rect.collidepoint(mouse_pos):
                    # Вход в 8 уровень
                    print("сасиски8")

        current_time = time.time()

        if current_time - start_time <= 3:
            draw(screen)
            pixiles(screen)
        else:
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()
