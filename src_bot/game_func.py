import json

from src_common.boardstate import BoardState
from src_common.ai import AI
import settings.game_settings as game_set

from src_bot.bot_gui import show_board
from src_bot.bot_init import bot
import text_data.phrases as text


def load_game(user_id: str) -> 'BoardState':
    board = BoardState.load_user(user_id)
    return board


def can_continue_game(user_id: str) -> 'bool':
    with open(game_set.user_id_file_name, "r") as user_id_list:
        available_players = json.load(user_id_list)
    if user_id in available_players:
        return available_players[user_id]
    else:
        available_players[user_id] = False
        with open(game_set.user_id_file_name, "w") as user_id_list:
            json.dump(available_players, user_id_list)
        return False


def start_new_game(user_id: str) -> 'BoardState':
    with open(game_set.user_id_file_name, "r") as user_id_list:
        available_players = json.load(user_id_list)
    available_players[user_id] = True
    with open(game_set.user_id_file_name, "w") as user_id_list:
        json.dump(available_players, user_id_list)

    board = BoardState.initial_state()
    board.save_user(user_id)
    return board


def get_correct_turn_command(command: list,
                             board: 'BoardState') -> 'Optional[list]':
    cords = []
    if len(command) != 3:
        return None
    try:
        cords.append(int(command[1]))
        cords.append(int(command[2]))
    except ValueError:
        return None

    if (0 <= cords[0] < game_set.board_size and
            0 <= cords[1] < game_set.board_size and
            board.board[cords[0], cords[1]] == 0):
        return cords
    else:
        return None


def finish_game(user_id: int, board: 'BoardState'):
    show_board(board, user_id)
    if board.is_first_player_turn:
        bot.send_message(user_id, text.win_text)
    else:
        bot.send_message(user_id, text.lose_text)


def make_ai_turn(user_id: 'int', board: 'BoardState', ai: 'AI'):
    board = ai.next_move(board, None)[0]
    board.save_user(str(user_id))

    if board.is_game_finished:
        finish_game(user_id, board)
        return

    show_board(board, user_id)
