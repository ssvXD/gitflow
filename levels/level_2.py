import pygame
import sys

import enviroment
from enviroment import ENV

pygame.init()

# Initialize all_sprites group
all_sprites = pygame.sprite.Group()


def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {filename}. Ошибка: {e}")
        sys.exit()


# AnimatedSprite class definition
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.moving = False
        self.left = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_jumping = False
        self.jump_count = 10
        self.original_y = y
        self.mask = pygame.mask.from_surface(self.image)  # Создаем маску
        self.gravity = 0.5  # Сила гравитации
        self.velocity_y = 0  # Скорость по вертикали

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]

        if self.is_jumping:
            self.jump()

        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверка на столкновение с землей (стенами)
        self.check_collision_with_walls()

    def jump(self):
        if self.jump_count >= -10:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            self.rect.y -= (self.jump_count ** 2) * 0.1 * neg
            self.jump_count -= 1
        else:
            self.is_jumping = False
            self.jump_count = 10
            self.velocity_y = 0  # Сбрасываем скорость после прыжка

    def check_collision_with_walls(self):
        # Проверяем, находится ли персонаж на стене
        on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity_y > 0:  # Если персонаж падает вниз
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                    on_ground = True
                elif self.velocity_y < 0:  # Если персонаж движется вверх
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

        # Если персонаж не на земле, он падает
        if not on_ground and not self.is_jumping:
            self.velocity_y += self.gravity
        else:
            self.velocity_y = 0


class FireSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.moving = False
        self.left = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1  # Скорость анимации
        self.last_update = pygame.time.get_ticks()
        self.x = x  # Сохраняем координату x
        self.y = y  # Сохраняем координату y
        self.mask = pygame.mask.from_surface(self.image)  # Создаем маску

    def cut_sheet(self, sheet, columns, rows):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, frame_width, frame_height)

        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
                # Убедитесь, что вы не выходите за пределы изображения
                if (frame_location[0] + frame_width <= sheet.get_width() and
                        frame_location[1] + frame_height <= sheet.get_height()):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 99:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]

        # Убедитесь, что у вашего изображения есть прозрачный фон
        self.image.set_colorkey((0, 0, 0))  # Установите цвет ключа для прозрачности


# Load images
dragon_sheet1 = load_image("./AnimationSheet_Character.png")
dragon_sheet2 = load_image("./AnimationSheet_Character2.png")
background_image = load_image("./back.jpg")
fire_sheet = load_image("./ff-Photoroom.png")

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
WALL_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (128, 0, 0)
START_COLOR = (128, 0, 0)
END_COLOR = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт в аду")

walls = [
    pygame.Rect(50, 190, 100, 20),
    pygame.Rect(220, 300, 100, 20),
    pygame.Rect(50, 510, 100, 20),
    pygame.Rect(220, 510, 100, 20),
    pygame.Rect(390, 510, 100, 20),
    pygame.Rect(560, 510, 100, 20)
]

start_point = pygame.Rect(50, 50, 50, 50)
end_point = pygame.Rect(700, 500, 50, 50)

# Create a single dragon character
# Create a single dragon character
dragon = AnimatedSprite(dragon_sheet1, 8, 1, 50, 50)
fire = FireSprite(fire_sheet, 9, 1, 150, 0)  # Огонь 1 остается наверху
fire2 = FireSprite(fire_sheet, 9, 1, 155, 320)  # Огонь 2 опущен между стенами
fire3 = FireSprite(fire_sheet, 9, 1, 325, 320)  # Огонь 3 опущен между стенами
fire4 = FireSprite(fire_sheet, 9, 1, 510, 320)

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)


def draw_start_end():
    pygame.draw.rect(screen, START_COLOR, start_point)
    pygame.draw.rect(screen, END_COLOR, end_point)


def game_over_screen(screen):
    screen.fill(GAME_OVER_COLOR)
    font = pygame.font.Font(None, 74)
    text = font.render("Игра окончена!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    ENV.display_screen = 0


def level_2(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENV.display_screen = None
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dragon.is_jumping:  # Прыжок только если на земле
                    dragon.is_jumping = True
                    dragon.original_y = dragon.rect.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # Move right
            dragon.rect.x += 5
            dragon.left = False
            dragon.moving = True
        elif keys[pygame.K_a]:  # Move left
            dragon.rect.x -= 5
            dragon.left = True
            dragon.moving = True
        else:
            dragon.moving = False

        # Проверка на заход в координаты огня через маски
        offset = (fire.rect.x - dragon.rect.x, fire.rect.y - dragon.rect.y)
        offset2 = (fire2.rect.x - dragon.rect.x, fire2.rect.y - dragon.rect.y)
        offset3 = (fire3.rect.x - dragon.rect.x, fire3.rect.y - dragon.rect.y)
        if dragon.mask.overlap(fire.mask, offset) or dragon.mask.overlap(fire2.mask, offset2) or dragon.mask.overlap(fire3.mask, offset3):
            print("Игрок столкнулся с огнем!")  # Отладочное сообщение
            game_over_screen(screen)
            ENV.display_screen = 1
            return

        # Проверка на столкновение со стенами
        for wall in walls:
            if dragon.rect.colliderect(wall):
                if dragon.velocity_y > 0:  # Если персонаж падает вниз
                    dragon.rect.bottom = wall.top
                    dragon.velocity_y = 0

        # Проверка на достижение конечной точки
        if dragon.rect.colliderect(end_point):
            screen.fill((0, 128, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("Вы остались живы!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            enviroment.counter += 1
            ENV.display_screen = 0
            return

        screen.blit(background_image, (0, 0))
        draw_walls()
        draw_start_end()

        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    level_2(screen)