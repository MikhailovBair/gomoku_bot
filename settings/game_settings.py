board_size = 15
win_len = 5

display_size = 600

ai_search_depth = 2

basic_vectors = ((1, 0), (0, 1), (1, 1), (1, -1))
interesting_zone = ((-2, 0), (-1, -1), (0, -2), (1, -1), (2, 0),
                    (1, 1), (0, 2), (-1, 1), (1, 0), (-1, 0), (0, 1), (1, 0))

is_ai_enabled: bool = True
first_player_is_ai: bool = True

save_file_name = "saves/savefile"
user_id_file_name = "saves/user_id.json"
pickle_suffix = ".pickle"
