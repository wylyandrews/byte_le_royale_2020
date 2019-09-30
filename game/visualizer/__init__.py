# import sys
# import math
# import random
# import time
# import zipfile
#
# import pygame
# from pygame.locals import *
#
# from game.visualizer.game_log_parser import GameLogParser
# from game.utils.helpers import *
# from game.common.enums import *
# from game.visualizer.graphs import *
# from game.config import *
# from game.common.stats import *
# from game.visualizer.city_sprites import *
# from game.visualizer.location_sprites import *
#
# pause = False
# log_parser = None
# global_surf = None
# fpsClock = None
#
# turn = 0 # current turn of the visualizer
# # List that stores population information
# population_list = []
#
#
# debug = False
#
# # Sprite Groups
# city_group = pygame.sprite.Group()
# location_group = pygame.sprite.Group()
#
# _VIS_INTERMEDIATE_FRAMES = VIS_INTERMEDIATE_FRAMES
# _FPS = FPS
#
#
# def log(msg):
#     if debug:
#         print(str(msg))
#
#
# def start(gamma, fullscreen=False):
#     global pause
#     global fpsClock
#     global log_parser
#     global turn
#
#
#     log_parser = GameLogParser("logs/")
#
#     # initialize pygame
#     pygame.init()
#     fpsClock = pygame.time.Clock()
#     pygame.font.init()
#
#     global global_surf
#     if fullscreen:
#         global_surf = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
#     else:
#         global_surf = pygame.display.set_mode(DISPLAY_SIZE)
#     pygame.display.set_caption('Byte-le Royale: Disaster Dispatcher')
#
#     pygame.display.set_gamma(gamma)
#
#     # Sprite changing logic
#     city_x = 484
#     city_y = 200
#     city_struct = GameStats.city_structure
#
#     # Checks city_structure and draws sprite accordingly
#     if city_struct <= GameStats.city_structure / 3:
#         city_sprite = CitySpriteLevel0(city_x, city_y, CityLevel.level_zero)
#         city_group.add(city_sprite)
#     elif city_struct <= GameStats.city_structure / 2:
#         city_sprite = CitySpriteLevel0(city_x, city_y, CityLevel.level_one)
#         city_group.add(city_sprite)
#     elif city_struct <= GameStats.city_structure:
#         city_sprite = CitySpriteLevel0(city_x, city_y, CityLevel.level_two)
#         city_group.add(city_sprite)
#
#     location_sprite = LocationDefault(0,0, CityLocation.default)
#     location_group.add(location_sprite)
#
#     # prep for game loop
#     turn_wait_counter = 1
#
#     # the big boy
#     while True:
#
#         handle_events()
#
#         if not pause:
#             # increment forward and display page
#             turn += 1
#             show()
#
#
# # Update the visualizer to display the current turn data
# def show():
#     global turn
#     draw_screen(turn)
#     pygame.display.update()
#     fpsClock.tick(_FPS)
#
#
# def draw_screen(current_turn):
#     global global_surf
#     global log_parser
#     global turn
#
#     # clear screen
#     global_surf.fill(pygame.Color(128, 212, 255))
#
#     # Draw groups
#     location_group.draw(global_surf)
#     city_group.draw(global_surf)
#
#
#     # This is all trash for testing
#     font = pygame.font.SysFont(pygame.font.get_default_font(), 30, True)
#
#     turn_info = log_parser.get_turn(current_turn)
#     if turn_info is None:
#         endgame()
#     turn_indicator = font.render(f'Turn {turn}', True, (150, 140, 130))
#
#     #List to keep track of population information
#     population_list.append(int(turn_info['player'].get('city').get('population')))
#
#     health_bar(turn_info, global_surf)
#     global_surf.blit(turn_indicator, (30, 500))
#
#     # Display actual rates
#     n = 0
#     for key, item in turn_info['rates'].items():
#         n += 1
#         text = f'{key}: {item}'
#         render_text = font.render(text, True, (0, 150, 150))
#         global_surf.blit(render_text, (30, 30*n))
#
#     # Display city sensor rates
#     n = 0
#     for sensor in turn_info['player']['city']['sensors'].values():
#         n += 1
#         text = f'{sensor["sensor_type"]}: {sensor["sensor_results"]}'
#         render_text = font.render(text, True, (0, 150, 150))
#         global_surf.blit(render_text, (500, 30*n))
#
#
# # Display endgame screen
# def endgame():
#     global_surf.fill(pygame.Color(0, 255, 255))
#     font = pygame.font.SysFont('Comic Sans MS', 30)
#     text_surface = font.render('Some Text', False, (0, 0, 0))
#     global_surf.blit(text_surface,(0,0))
#     # Draws graph of round's data
#     line_graph_surface = lineGraph(population_list, 500,250)
#
#
#     global_surf.blit(line_graph_surface,(300,300))
#
#     pygame.display.update()
#
#     # Stays running till exit button pressed
#     while True:
#         handle_events()
#
#
# def handle_events():
#     for event in pygame.event.get():
#         # Application exited by user
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#
#         # Keyboard events
#         elif event.type == KEYUP:
#             global turn
#
#             # Pause toggle
#             if event.key == K_p:
#                 global pause
#                 pause = not pause
#
#             # Toggle fullscreen (may not work on windows)
#             if event.key == K_f:
#                 pygame.display.toggle_fullscreen()
#
#             # Exit
#             if event.key == K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
#
#             # Back up a turn
#             if event.key == K_LEFT:
#                 turn -= 1
#                 show()
#
#             # Forward a turn
#             if event.key == K_RIGHT:
#                 turn += 1
#                 show()
#
#             # start
#             if event.key == K_DOWN:
#                 turn = 1
#                 show()
#
#             # end
#             if event.key == K_UP:
#                 turn = MAX_TURNS
#                 show()
#
#             # yeet
#             if event.key == K_y:
#                 turn = random.randint(1, MAX_TURNS)
#                 show()

import cocos
from cocos.director import director
import pyglet

from game.config import *
from game.visualizer.game_log_parser import GameLogParser
from game.visualizer.graphs import *
from game.visualizer.city_sprites import *
from game.visualizer.location_sprites import *
from game.visualizer.health_bar import *
from game.visualizer.time_layer import *
from game.visualizer.end_layer import *

size = DISPLAY_SIZE
log_parser = None
turn = 1


def start(gamma, fullscreen=False):
    global log_parser
    global turn

    log_parser = GameLogParser("logs/")

    # initialize cocos
    director.init(width=size[0], height=size[1], caption="Byte-le Royale: Disaster Dispatcher", fullscreen=fullscreen)

    # Get turn info from logs, if None go to end scene
    turn_info = log_parser.get_turn(turn)
    if turn_info is None:
        end = EndLayer(size)
        end_scene = cocos.scene.Scene().add(end)
        director.replace(end_scene)
    else:
        # Initialize clock layer and add an interval
        clock = TimeLayer(size, turn_info, turn)
        clock.schedule_interval(callback=timer, interval=0)

        first_scene = create_scene(turn_info)
        first_scene.add(clock)

        director.run(first_scene)


def timer(interval):
    global turn
    turn += 1
    director.scene_stack.clear()

    turn_info=log_parser.get_turn(turn)
    if turn_info is None:
        end = EndLayer(size)
        end_scene = cocos.scene.Scene().add(end)
        director.replace(end_scene)
    else:
        clock = TimeLayer(size, turn_info, turn)
        clock.schedule_interval(callback=timer, interval=0.1)

        current_scene = create_scene(turn_info)
        current_scene.add(clock)

        director.replace(current_scene)


def create_scene(info):
    # Generate layers
    health_layer = HealthBar(size, info)
    location_layer = LocationLayer(size, 'plains')
    city_layer = CityLayer(size, info)

    # Add layers to
    scene = cocos.scene.Scene()
    scene.add(location_layer, 0)
    scene.add(city_layer, 1)
    scene.add(health_layer, 1)

    return scene

