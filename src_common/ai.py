from itertools import product
from typing import Optional

from src_common.boardstate import BoardState
import settings.game_settings as game_set
from evaluation_settings.eval_parameter import eval_score


class PositionEvaluation:
    def __call__(self, board: BoardState) -> float:
        basic_value = [0] * game_set.win_len
        balance: float = 0
        for y, x in product(range(game_set.board_size),
                            range(game_set.board_size)):

            for vector in game_set.basic_vectors:
                max_y = y + vector[0] * (game_set.win_len - 1)
                max_x = x + vector[1] * (game_set.win_len - 1)
                if BoardState.is_coord_correct(max_y, max_x):
                    for diff in range(game_set.win_len):
                        basic_value[diff] = board.board[y + vector[0] * diff,
                                                        x + vector[1] * diff]

                    key_tuple = tuple(basic_value)
                    balance += eval_score[key_tuple]

        return balance


class AI:
    def __init__(self, position_evaluation: PositionEvaluation =
                 PositionEvaluation(),
                 search_depth: int = game_set.ai_search_depth):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.depth: int = search_depth

    def next_move(self, board: BoardState, top_res: Optional['int']) -> \
            (Optional[BoardState], float):
        if self.depth == 0:
            return board, self.position_evaluation(board)

        moves = board.get_good_possible_moves()
        best_value = None
        best_board = None
        board_config = board.is_first_player_turn ^ 1
        for move in moves:
            cur_board, cur_score = AI(self.position_evaluation,
                                      self.depth - 1).next_move(move,
                                                                best_value)
            if cur_board is None:
                continue

            if top_res is not None and ((top_res > cur_score) == board_config):
                return None, 0

            if best_value is None or (best_value > cur_score) == board_config:
                best_board, best_value = move, cur_score
        return best_board, best_value
