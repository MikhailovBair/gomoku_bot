from itertools import product

import pygame
from pygame import Surface

from src_common.boardstate import BoardState
import settings.game_settings as game_set
import settings.gui_settings as gui_set


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int,
               board: BoardState):
    for y, x in product(range(game_set.board_size), range(game_set.board_size)):
        color = gui_set.white_board_color if (x + y) % 2 == 0 else \
            gui_set.black_board_color
        position = (pos_x + x * elem_size, pos_y + y * elem_size,
                    elem_size, elem_size)
        pygame.draw.rect(screen, color, position)
        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = gui_set.white_figure_color
        else:
            figure_color = gui_set.black_figure_color
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color,
                           (position[0] + elem_size // 2,
                            position[1] + elem_size // 2), r)

    if board.notification:
        font = pygame.font.SysFont('None', gui_set.font_size)
        text = font.render(board.notification, True, gui_set.font_color)
        text_rect = text.get_rect()
        text_rect.center = (game_set.display_size // 2,
                            game_set.display_size // 2)
        screen.blit(text, text_rect)
