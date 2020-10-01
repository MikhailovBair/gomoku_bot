import pygame
from pygame import Surface

import settings.game_settings as game_set
from src_common.boardstate import BoardState
from src_common.ai import AI
from desktop.src_desktop.gui import draw_board


def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // game_set.board_size

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = [p // grid_size for p in event.pos]
                if event.button == 1:  # do move
                    board.notification = None
                    board = board.do_move(y, x)
                elif event.button == 3:  # change figure
                    board.board[y, x] = ((board.board[y, x] + 2) % 3) - 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = BoardState.initial_state()

                if event.key == pygame.K_s:
                    board.save()

                if event.key == pygame.K_l:
                    board = BoardState.load()

                if event.key == pygame.K_z:
                    pass

                if (game_set.is_ai_enabled and event.key == pygame.K_SPACE and
                        game_set.first_player_is_ai ==
                        board.is_first_player_turn):
                    new_board = ai.next_move(board, None)[0]
                    if new_board is not None:
                        board = new_board

        if board.is_game_finished:
            board.notification = "Second" if board.is_first_player_turn \
                else "First"
            board.notification += " player won! Press R to restart"

        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()
