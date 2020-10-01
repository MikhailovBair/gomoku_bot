from src_common.boardstate import BoardState
import settings.game_settings as game_set
import settings.gui_bot_settings as gui_bot
from src_bot.bot_init import bot


def show_board(board: BoardState, user_id: int):
    board_picture = []
    for y in range(game_set.board_size):
        for x in range(game_set.board_size):
            figure = board.board[y, x]
            if figure == 0:
                board_picture.append(gui_bot.board_piece)
            elif figure > 0:
                board_picture.append(gui_bot.white_piece)
            else:
                board_picture.append(gui_bot.black_piece)
        board_picture.append("\n")

    board_to_emoji = ''.join(board_picture)
    bot.send_message(user_id, board_to_emoji)

