import pygame
import sys
from enviroment import ENV

pygame.init()

# Initialize all_sprites group
all_sprites = pygame.sprite.Group()


def load_image(filename):
    try:
        image = pygame.image.load(filename).convert_alpha() #convert_alpha добавит прозрачность
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
        self.original_y = y

        # --- Гравитация ---
        self.gravity = 0.5  # Сила гравитации
        self.y_velocity = 0  # Скорость по оси Y (вертикальная)
        self.jump_force = -10  # Величина прыжка (отрицательная, т.к. вверх)
        self.on_ground = False #Флаг, чтобы знать, находится ли персонаж на земле

        # --- Хитбокс ---
        self.mask = pygame.mask.from_surface(self.image)  # Создаем маску
        self.rect = self.mask.get_rect(center=self.rect.center) # Выравниваем хитбокс по маске

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        # Анимация
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]

        # --- Гравитация ---
        if not self.on_ground:  # Применяем гравитацию только если не на земле
            self.y_velocity += self.gravity  # Применяем гравитацию
            # Максимальная скорость падения (чтобы не улетел за карту)
            if self.y_velocity > 10:
                self.y_velocity = 10
            self.rect.y += self.y_velocity  # Изменяем положение по Y

        # --- Прыжок ---
        if self.is_jumping:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_force  # Даем начальную скорость вверх
        self.is_jumping = False # Сбрасываем флаг прыжка сразу после толчка


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
dragon_sheet1 = load_image("AnimationSheet_Character.png")
dragon_sheet2 = load_image("AnimationSheet_Character2.png")
background_image = load_image("back.jpg")
fire_sheet = load_image("ff-Photoroom.png")

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

# --- Усложнение: Добавляем платформы ---
platforms = [
    pygame.Rect(0, 500, 200, 20),  # Платформа слева
    pygame.Rect(300, 400, 200, 20),  # Платформа в центре
    pygame.Rect(600, 300, 200, 20)   # Платформа справа
]

# --- Заменяем стены на более сложные ---
walls = [
    pygame.Rect(50, 190, 100, 20),
    pygame.Rect(200, 190, 100, 20),
    pygame.Rect(350, 190, 100, 20),
    pygame.Rect(500, 190, 100, 20),
    pygame.Rect(590, 540, 100, 20),
    pygame.Rect(700, 450, 20, 100), # Вертикальная стена
    pygame.Rect(0, 100, 20, 200)    # Еще одна вертикальная стена
]

start_point = pygame.Rect(50, 50, 50, 50)
end_point = pygame.Rect(700, 500, 50, 50)

# Create a single dragon character
dragon = AnimatedSprite(dragon_sheet1, 8, 1, 50, 50)
fire = FireSprite(fire_sheet, 9, 1, 150, 0)  # Создаем спрайт огня
fire2 = FireSprite(fire_sheet, 9, 1, 300, 0)
fire3 = FireSprite(fire_sheet, 9, 1, 450, 0)


def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, (100, 100, 100), platform)  # Серый цвет для платформ

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


def level_1(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENV.display_screen = None
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dragon.on_ground: # Прыгаем только если на земле
                    dragon.is_jumping = True # Включаем флаг прыжка
                    dragon.on_ground = False  # Теперь мы не на земле
                    dragon.y_velocity = dragon.jump_force  # Даем начальную скорость вверх

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

        # --- Коллизия с платформами и полом + Гравитация---
        dragon.on_ground = False  # Сбрасываем флаг "на земле" в начале каждого кадра

        # Сохраняем старую позицию для отката
        old_x = dragon.rect.x
        old_y = dragon.rect.y

        # Сначала двигаем персонажа по вертикали (гравитация/прыжок)
        dragon.update()

        # Проверяем коллизию с платформами
        for platform in platforms:
            if dragon.rect.colliderect(platform):
                # Если столкнулись сверху
                if old_y + dragon.rect.height <= platform.top:
                    dragon.rect.bottom = platform.top
                    dragon.y_velocity = 0
                    dragon.on_ground = True

        # Проверяем коллизию с полом
        if dragon.rect.bottom >= HEIGHT:
            dragon.rect.bottom = HEIGHT
            dragon.y_velocity = 0
            dragon.on_ground = True

        # Если ни с чем не столкнулись, значит, в воздухе
        if not dragon.on_ground:
            dragon.y_velocity += dragon.gravity

        # --- Горизонтальное движение и коллизии со стенами ---
        player_rect = dragon.rect.copy()  # Копия для проверки столкновений

        if keys[pygame.K_d]:
            player_rect.x += 5
        elif keys[pygame.K_a]:
            player_rect.x -= 5

        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_d]:
                    player_rect.right = wall.left
                elif keys[pygame.K_a]:
                    player_rect.left = wall.right

        dragon.rect.x = player_rect.x  # Применяем горизонтальное движение

        # --- Вертикальное движение и коллизии с платформами и полом ---
        # Вертикальное движение уже обработано в dragon.update() и проверках выше

        # Проверка на заход в координаты огня через маски
        offset = (fire.rect.x - dragon.rect.x, fire.rect.y - dragon.rect.y)
        if dragon.mask.overlap(fire.mask, offset):
            print("Игрок столкнулся с огнем!")  # Отладочное сообщение
            game_over_screen(screen)
            ENV.display_screen = 1
            return

        # Проверка на достижение конечной точки
        if player_rect.colliderect(end_point):
            screen.fill((0, 128, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("You are alive", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
            ENV.display_screen = 0
            return

        screen.blit(background_image, (0, 0))
        draw_walls()
        draw_platforms()
        draw_start_end()

        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    level_1(screen)
