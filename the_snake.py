import random

import pygame

# ===== ГЛОБАЛЬНЫЕ КОНСТАНТЫ И ПЕРЕМЕННЫЕ =====
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = None
clock = None
# =============================================


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None):
        """Инициализирует игровой объект."""
        self.position = position if position else (0, 0)
        self.body_color = None

    def draw(self, surface):
        """Отрисовывает объект на поверхности."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.length = 1
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на поверхности."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
        if len(self.positions) > self.length:
            last_pos = self.positions[-1]
            erase_rect = pygame.Rect(
                last_pos[0],
                last_pos[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, erase_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True


def main():
    """Основная функция игры."""
    pygame.init()
    global screen, clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        for segment in snake.positions[1:]:
            if snake.get_head_position() == segment:
                snake.reset()
                apple.randomize_position()
                break

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
