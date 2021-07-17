import pygame
import time

from snake import Snake
from ai import *
from supercellerator import ai_supercellerator_v1

###############################################################################

# def test_thing():
#     a = ()
#     keep_alive = []
#     for x in range(20000):
#         a = (x, a)
#         b = (x * 2, a)
#         keep_alive.append(b)

#     count = 0
#     for x in keep_alive:
#         count += 1
#     summation = 0
#     current = a
#     while current:
#         summation += current[0]
#         current = current[1]
    
#     print('count is: ' + str(count))
#     print('sum is: ' + str(summation))

# start = time.time()
# test_thing()
# end = time.time()
# print('Time taken: ' + str(end - start))

# exit()

###############################################################################

pygame.init()

###############################################################################

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

GAME_WIDTH = 30
GAME_HEIGHT = 30

DELAY = 2

###############################################################################

screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
pygame.display.set_caption("Snake")

snake_game = Snake(GAME_WIDTH, GAME_HEIGHT)

# Debug impossible situation
# snake_game.goal = (0, 0)
# snake_game.snake_position = deque([
#     (7,7),
#     (6,7),
#     (6,6),
#     (6,5),
#     (6,4),
#     (6,3),
#     (6,2),
#     (6,1),
#     (6,0),
#     (5,0),
#     (5,1),
#     (5,2),
#     (5,3),
#     (5,4),
#     (5,5),
#     (5,6),
#     (5,7),
#     (4,7),
#     (4,6),
#     (4,5),
#     (4,4),
#     (4,3),
#     (4,2),
#     (4,1),
#     (4,0),
# ])


# Debug hard situation
# snake_game.goal = (0, 7)
# snake_game.snake_position = deque([
#     (3,4),
#     (3,3),
#     (3,2),
#     (3,1),
#     (4,1),
#     (4,0),
#     (3,0),
#     (2,0),
#     (1,0),
#     (0,0),
#     (0,1),
#     (1,1),
#     (1,2),
#     (1,3),
#     (1,4),
#     (1,5),
#     (1,6),
#     (1,7),
#     (2,7),
#     (3,7),
#     (4,7),
#     (5,7),
#     (6,7),
#     (7,7),
#     (7,6),
#     (7,5),
#     (7,4),
#     (7,3),
#     (6,3),
#     (5,3),
#     (5,2),
#     (5,1),
#     (5,0),
# ])

running = True
printed_result = False
last_tick = 0

while snake_game.get_state() == Snake.PLAYING:
    snake_game.advance(ai_supercellerator_v1(snake_game))
    if snake_game.get_state() == Snake.WON:
        print('Victory in ' + str(snake_game.get_moves()) + ' moves!')
    elif snake_game.get_state() == Snake.DIED:
        print('Snake died')

# snake_game.render(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
# pygame.display.flip()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     now = pygame.time.get_ticks()
#     state = snake_game.get_state()
#     if state == Snake.PLAYING:
#         if now > last_tick + DELAY:
#             snake_game.advance(ai_supercellerator_v1(snake_game))
#             last_tick = now
#     elif not printed_result:
#         if state == Snake.WON:
#             print('Victory in ' + str(snake_game.get_moves()) + ' moves!')
#         elif state == Snake.DIED:
#             print('Snake died')
#         printed_result = True

#     snake_game.render(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
#     pygame.display.flip()

# pygame.quit()