import settings.game_settings as game_set
from src_common.ai import AI, PositionEvaluation
from src_common.boardstate import BoardState

import src_bot.game_func as gf
from src_bot.bot_init import bot
import text_data.phrases as text
from src_bot.bot_gui import show_board

ai = AI(PositionEvaluation(), game_set.ai_search_depth)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.from_user.id, text.help_text)


@bot.message_handler(commands=['start'])
def game_menu(message):
    bot.send_message(message.from_user.id, text.start_text)


@bot.message_handler(commands=['new_game'])
def new_game(message):
    board = gf.start_new_game(str(message.from_user.id))
    gf.make_ai_turn(message.from_user.id, board, ai)


@bot.message_handler(commands=['continue'])
def continue_game(message):
    user_id = message.from_user.id
    if gf.can_continue_game(str(user_id)):
        board = gf.load_game(str(user_id))
        board.save_user(str(user_id))
        show_board(board, user_id)
        bot.send_message(user_id, text.continue_game_text)
    else:
        bot.send_message(user_id, text.no_game_text)


@bot.message_handler(commands=['turn'])
def make_turn(message):
    user_id = message.from_user.id
    board = BoardState.load_user(str(user_id))

    if board.is_game_finished:
        bot.send_message(user_id, text.start_new_game_text)
        return

    cords = gf.get_correct_turn_command(message.text.split(), board)

    if cords is None:
        bot.send_message(user_id, text.bad_move_text)
        return

    board = board.do_move(cords[0], cords[1])
    if board.is_game_finished:
        gf.finish_game(user_id, board)
        return

    gf.make_ai_turn(user_id, board, ai)


bot.polling(none_stop=True, interval=0)
