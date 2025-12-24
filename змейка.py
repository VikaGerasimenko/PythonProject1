import random

import pygame


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
        x = random.randint(0, 31) * 20
        y = random.randint(0, 23) * 20
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = (20, 0)
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
        new_x = (head_x + dx) % 640
        new_y = (head_y + dy) % 480
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на поверхности."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], 20, 20)
            pygame.draw.rect(surface, self.body_color, rect)
        if len(self.positions) > self.length:
            last_pos = self.positions[-1]
            erase_rect = pygame.Rect(last_pos[0], last_pos[1], 20, 20)
            pygame.draw.rect(surface, (0, 0, 0), erase_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = (20, 0)
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 20):
                snake.next_direction = (0, -20)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -20):
                snake.next_direction = (0, 20)
            elif event.key == pygame.K_LEFT and snake.direction != (20, 0):
                snake.next_direction = (-20, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-20, 0):
                snake.next_direction = (20, 0)
    return True


def main():
    """Основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
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

        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
