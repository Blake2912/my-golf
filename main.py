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
    hypotenuse = x_len*x_len + y_len*y_len
    return math.sqrt(hypotenuse)


def check_inside_circle(x, y, radius, h, k):
    val = (x-h)**2 + (y-k)**2 - radius**2
    if val <= 0.0:
        return True
    else:
        return False


# Player level variables and functions
player_x = 210
player_y = 320
player_circle_width = 10
player_color = (255, 255, 255)  # Color in RGB


def draw_player(x, y):
    pygame.draw.circle(screen, player_color, (x, y), player_circle_width)


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
        draw_player(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        print(pygame.mouse.get_pos())

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
            if check_inside_circle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], player_circle_width, player_x, player_y):
                if event.button == 1:  # Only left button is clicked
                    print("Inside object")
                    if_mouse_clicked = True
            # print("Mouse clicked on x:", pygame.mouse.get_pos()[0])
            # print("Mouse clicked on y:", pygame.mouse.get_pos()[1])
            # print("Player x: {0} Player y: {1}".format(player_x, player_y))
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if_mouse_clicked = False

    pygame.display.update()
