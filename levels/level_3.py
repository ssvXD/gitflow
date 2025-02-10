import pygame
import sys

import enviroment
from enviroment import ENV

pygame.init()

all_sprites = pygame.sprite.Group()


def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {filename}. Ошибка: {e}")
        sys.exit()


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
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0.5
        self.velocity_y = 0

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

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

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
            self.velocity_y = 0

    def check_collision_with_walls(self):
        on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity_y > 0:
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                    on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

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
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, frame_width, frame_height)

        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
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

        self.image.set_colorkey((0, 0, 0))


dragon_sheet1 = load_image("AnimationSheet_Character.png")
dragon_sheet2 = load_image("AnimationSheet_Character2.png")
background_image = load_image("back.jpg")
fire_sheet = load_image("ff-Photoroom.png")

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
    pygame.Rect(45, 445, 100, 20),
    pygame.Rect(192, 413, 100, 20),
    pygame.Rect(328, 386, 100, 20),
    pygame.Rect(458, 361, 100, 20),
    pygame.Rect(590, 540, 100, 20)
]

start_point = pygame.Rect(50, 50, 50, 50)
end_point = pygame.Rect(700, 500, 50, 50)

dragon = AnimatedSprite(dragon_sheet1, 8, 1, 50, 50)
fire = FireSprite(fire_sheet, 9, 1, 592, 278)


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
    pygame.time.delay(1000)
    ENV.display_screen = 0


def level_3(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENV.display_screen = None
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dragon.is_jumping:
                    dragon.is_jumping = True
                    dragon.original_y = dragon.rect.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dragon.rect.x += 5
            dragon.left = False
            dragon.moving = True
        elif keys[pygame.K_a]:
            dragon.rect.x -= 5
            dragon.left = True
            dragon.moving = True
        else:
            dragon.moving = False

        offset = (fire.rect.x - dragon.rect.x, fire.rect.y - dragon.rect.y)
        if dragon.mask.overlap(fire.mask, offset):
            game_over_screen(screen)
            ENV.display_screen = 0
            return

        for wall in walls:
            if dragon.rect.colliderect(wall):
                if dragon.velocity_y > 0:
                    dragon.rect.bottom = wall.top
                    dragon.velocity_y = 0

        if dragon.rect.colliderect(end_point):
            screen.fill((0, 128, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("Вы остались живы!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            enviroment.counter += 1
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            ENV.display_screen = 0
            return

        screen.blit(background_image, (0, 0))
        draw_walls()
        draw_start_end()

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    level_3(screen)
