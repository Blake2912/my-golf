import math
import random
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 640

# Screen Creation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game level variables
level_counter = 0
friction = 0  # NOTE:: The friction must change randomly in each level
if_mouse_clicked = False


def calculate_distance(x_len, y_len):
    hypotenuse = x_len * x_len + y_len * y_len
    return math.sqrt(hypotenuse)


def check_inside_circle(x, y, radius, h, k):
    val = (x - h) ** 2 + (y - k) ** 2 - radius ** 2
    if val <= 0.0:
        return True
    else:
        return False


def calculate_slope(x0, y0, x1, y1):
    fun_slope = 0
    try:
        fun_slope = (y1 - y0) / (x1 - x0)
    except ZeroDivisionError:
        fun_slope = (y1 - y0) / (x1 - (x0 + 1))
    return fun_slope


def calculate_y(x0, y0, x1, m):
    y = m * (x1 - x0) + y0
    return y


def calculate_x(x0, y0, y1, m):
    x = (y1 - y0) / m + x0
    return x


# Player level variables and functions
player_x = 210
player_y = 320
player_circle_width = 10
player_color = (255, 255, 255)  # Color in RGB
line_color = (205, 255, 10)
line_width = 5
playerMoveFlag = 0
endLineValue = ()
offset = 10
initial_line_click = ()


def draw_player(x, y):
    pygame.draw.circle(screen, player_color, (x, y), player_circle_width)


def draw_line(ini_pos, mouse_pos):
    pygame.draw.line(screen, line_color, ini_pos, mouse_pos, line_width)


# Hole Level variables and functions
hole_x = 100
hole_y = 200
hole_circle_width = 20
hole_color = (0, 255, 0)


def draw_hole(x, y):
    pygame.draw.circle(screen, hole_color, (x, y), hole_circle_width)


# This is the variable which will keep track if the game is running or not
isRunning = True

while isRunning:
    screen.fill((0, 0, 0))
    draw_player(player_x, player_y)
    draw_hole(hole_x, hole_y)

    if if_mouse_clicked:
        draw_line(initial_line_click, pygame.mouse.get_pos())

    if playerMoveFlag == 3:
        print("Move Player")
        slope = calculate_slope(player_x, player_y, endLineValue[0], endLineValue[1])
        print("Slope", slope)
        # There is some bug here check the algorithm to do,
        # one of the approaches may be to implement the bresenham's line drawing algorithm

        playerMoveFlag = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False  # This will quit the game
        if event.type == KEYDOWN:
            # TODO:: When the Ball hits the whole then it should change and not on key press
            if event.key == K_p:
                # Here we are generating random values on the boundary of 50 to 420 in x-axis and 50 to 540 in y-axis
                if calculate_distance(abs(hole_x - player_x), abs(hole_y - player_y)) < 150:
                    player_x = random.randint(50, 420) + 80
                    player_y = random.randint(50, 540) + 80
                    hole_x = random.randint(60, 320)
                    hole_y = random.randint(60, 540)
                else:
                    player_x = random.randint(50, 420)
                    player_y = random.randint(50, 540)
                    hole_x = random.randint(60, 320)
                    hole_y = random.randint(60, 540)

            if event.key == K_ESCAPE:
                isRunning = False  # Pressing ESC will quit the game

        if event.type == MOUSEBUTTONDOWN:
            if check_inside_circle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], player_circle_width, player_x,
                                   player_y):
                if event.button == 1:  # Only left button is clicked
                    if_mouse_clicked = True
                    playerMoveFlag = 0
                    initial_line_click = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if_mouse_clicked = False
                # Storing the start and end points
                endLineValue = pygame.mouse.get_pos()
                playerMoveFlag = 3

    pygame.display.update()
