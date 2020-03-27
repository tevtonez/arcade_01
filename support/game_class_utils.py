# Python imports
# Third-Party imports
import arcade
# Project imports
from support import consts
from sprite_support.character import character_sprite


def setup_flags(window_instance):
    window_instance.score = 0

    # Set up the character at specific coordinates.
    window_instance.player_sprite, window_instance.player_list = character_sprite.make_player_sprite(
        window_instance.player_sprite,
        window_instance.player_list
    )
    window_instance.player_fell_sound_play = False
    window_instance.player_died = False
    window_instance.game_over = False
    window_instance.draw_game_over = False
    window_instance.play_win_sound = False
    window_instance.show_help_menu = False


def init_sounds(window_instance):
    window_instance.collect_coin_sound = arcade.load_sound(
        "sound/coins/coin_1.wav")
    window_instance.jump_sound = arcade.load_sound("sound/player/jump_1.wav")
    window_instance.scream_sound = arcade.load_sound('sound/player/fall_2.wav')
    window_instance.level_back_melody = arcade.load_sound(
        "sound/game/level_1.wav")
    window_instance.win_sound = arcade.load_sound('sound/game/win_1.wav')
    window_instance.lost_sound = arcade.load_sound('sound/game/lost_1.wav')


def init_flags(window_instance):
    # These are 'lists' that keep track of our sprites. Each sprite should go into a list.
    window_instance.player_list = None
    window_instance.coin_list = None
    window_instance.wall_list = None

    # Separate variable that holds the player sprite
    window_instance.player_sprite = None

    # Our physics engine
    window_instance.physics_engine = None

    # Used to keep track of our scrolling
    window_instance.view_bottom = 0
    window_instance.view_left = 0
    window_instance.score_text_position_x = 0
    window_instance.score_text_position_y = 0

    # coins counter (eg points)
    window_instance.score = None
    # other
    window_instance.block_keys = False
    window_instance.block_movement_keys = False
