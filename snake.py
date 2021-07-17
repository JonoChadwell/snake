import collections
import itertools
import pygame
import random

import common

class Snake:

    PLAYING = 1
    WON = 2
    DIED = 3

    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)
    VALID_DIRECTIONS = [NORTH, SOUTH, WEST, EAST]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = Snake.PLAYING
        self.snake_position = collections.deque([
            (width // 2, height // 2),
            (width // 2, height // 2),
            (width // 2, height // 2)])
        self.goal = self.generate_goal()
        self.moves = 0
        self.points = 0
        self.moves_since_point = 0

        # Rendering variables
        self.font = None
        self.win_text = None
        self.lose_text = None
        self.ai_data = None

    def copy(self):
        other = Snake(self.width, self.height)
        other.state = Snake.PLAYING
        other.snake_position = self.snake_position.copy()
        other.goal = self.goal
        other.moves = self.moves
        other.points = self.points
        other.moves_since_point = self.moves_since_point
        return other

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_state(self):
        return self.state

    def get_goal(self):
        return self.goal
    
    def get_snake_position(self):
        return self.snake_position

    def get_snake_head(self):
        return self.snake_position[0]

    def get_snake_tail(self):
        return self.snake_position[-1]

    def get_moves(self):
        return self.moves

    def get_moves_since_point(self):
        return self.moves_since_point

    def get_points(self):
        return self.points

    def get_ai_data(self):
        return self.ai_data

    def set_ai_data(self, value):
        self.ai_data = value

    def generate_goal(self):
        possibilities = []
        for x in range(self.width):
            for y in range(self.height):
                if (x,y) not in self.snake_position:
                    possibilities.append((x,y))
        if possibilities:
            return random.choice(possibilities)
        else:
            return None

    def advance(self, direction):
        if self.state != Snake.PLAYING:
            return

        self.moves += 1
        self.moves_since_point += 1

        if direction not in self.VALID_DIRECTIONS:
            self.state = Snake.DIED
            return

        if not self.is_direction_safe(direction):
            self.state = Snake.DIED
            return

        next = common.add_elements(self.snake_position[0], direction)
        
        self.snake_position.appendleft(next)

        if next == self.goal:
            self.points += 1
            self.moves_since_point = 0
            goal = self.generate_goal()
            if not goal:
                self.state = Snake.WON
                return
            self.goal = goal
        else:
            self.snake_position.pop()

    def is_direction_safe(self, direction):
        next = common.add_elements(self.snake_position[0], direction)
        if next in itertools.islice(self.snake_position, 0, len(self.snake_position) - 1):
            return False
        return common.in_bounds(next, (self.width, self.height))

    def render(self, screen, width, height):
        GOAL = (255,0,0)
        SNAKE_COLOR = (0, 255, 0)
        SNAKE_GAP_COLOR = (127, 200, 127)
        SNAKE_GAP_PORTION = 0.1

        BACKGROUND_COLOR = (50, 50, 50)
        WIN_TEXT_COLOR = (255, 0, 0)
        LOST_TEXT_COLOR = (255, 0, 0)

        if self.font is None:
            self.font=pygame.font.SysFont('timesnewroman',  30)
            self.win_text = self.font.render("You Win", True, WIN_TEXT_COLOR)
            self.lose_text = self.font.render("You Lose", True, LOST_TEXT_COLOR)


        screen.fill(BACKGROUND_COLOR)

        cell_size = min(width / self.width, height / self.height)
        gap = SNAKE_GAP_PORTION * cell_size

        last = None
        for pip in self.snake_position:
            pygame.draw.rect(screen, SNAKE_COLOR, [
                        cell_size * pip[0] + gap,
                        cell_size * pip[1] + gap,
                        cell_size - 2 * gap, 
                        cell_size - 2 * gap,
                    ])
            if last and last != pip:
                middle = common.average_elements(pip, last)
                w = cell_size - 2 * gap if pip[0] == last[0] else gap * 2 + 2
                h = gap * 2 + 2 if pip[0] == last[0] else cell_size - 2 * gap
                x = middle[0] * cell_size + cell_size / 2 - w / 2
                y = middle[1] * cell_size + cell_size / 2 - h / 2
                pygame.draw.rect(screen, SNAKE_GAP_COLOR, [x, y, w, h])


            last = pip

        pygame.draw.ellipse(screen, GOAL, [cell_size * self.goal[0], cell_size * self.goal[1], cell_size, cell_size])

        if self.state == Snake.DIED:
            screen.blit(self.lose_text, (100, 100))

        if self.state == Snake.WON:
            screen.blit(self.win_text, (100, 100))