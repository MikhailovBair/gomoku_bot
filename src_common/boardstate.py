from itertools import product
from typing import List

import numpy as np
import settings.game_settings as game_set
import pickle


class BoardState:
    def __init__(self, board: np.ndarray, is_first_player_turn: bool = True,
                 creator_mode=False, notification=None):
        self.board: np.ndarray = board
        self.is_first_player_turn: bool = is_first_player_turn
        self.creator_mode = creator_mode
        self.notification = notification

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.is_first_player_turn,
                          self.creator_mode, self.notification)

    @staticmethod
    def get_user_board_name(user_id: str) -> str:
        return game_set.save_file_name + user_id + game_set.pickle_suffix

    def save_user(self, user_id: str):
        with open(self.get_user_board_name(user_id), 'wb') as f:
            pickle.dump(self, f)

    def save(self, filename=game_set.save_file_name):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_user(user_id: str) -> 'BoardState':
        with open(BoardState.get_user_board_name(user_id), 'rb') as f:
            new_board_state = pickle.load(f)
        return new_board_state

    @staticmethod
    def load(filename=game_set.save_file_name):
        with open(filename, 'rb') as f:
            new_board_state = pickle.load(f)
        return new_board_state

    def do_move(self, y, x) -> 'BoardState':
        if self.board[y, x] != 0:  # invalid move
            self.notification = "This field is already occupied"
            return self.copy()

        result = self.copy()
        result.board[y, x] = 1 if self.is_first_player_turn else -1
        result.is_first_player_turn = not self.is_first_player_turn

        return result

    def get_good_possible_moves(self) -> List['BoardState']:
        possible_moves = []
        for y, x in product(range(game_set.board_size),
                            range(game_set.board_size)):
            if self.board[y, x] == 0:
                is_interesting = False
                for dy, dx in game_set.interesting_zone:
                    if (self.is_coord_correct(y + dy, x + dx) and
                            self.board[y + dy, x + dx] != 0):
                        is_interesting = True
                        break

                if is_interesting:
                    possible_moves.append(self.copy())
                    possible_moves[-1] = possible_moves[-1].do_move(y, x)
        return possible_moves

    @staticmethod
    def is_coord_correct(y: int, x: int) -> bool:
        return 0 <= y < game_set.board_size and 0 <= x < game_set.board_size

    @property
    def is_game_finished(self) -> bool:
        for y, x in product(range(game_set.board_size),
                            range(game_set.board_size)):
            if self.board[y, x] == 0:
                continue

            answers_for_win_pos = [True] + [False] * game_set.win_len + [True]
            for vector in game_set.basic_vectors:
                victory = True
                for diff in range(-1, game_set.win_len + 1):
                    new_y = y + vector[0] * diff
                    new_x = x + vector[1] * diff

                    if answers_for_win_pos[diff + 1] != \
                            (not BoardState.is_coord_correct(new_y, new_x) or
                             self.board[new_y, new_x] != self.board[y, x]):
                        victory = False
                        break

                if victory:
                    return victory
        return False

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(game_set.board_size, game_set.board_size),
                         dtype=np.int8)

        board[game_set.board_size // 2, game_set.board_size // 2] = -1
        # преимущественный ход чёрных 

        return BoardState(board, True, False)
