# Python imports
import time
# Third-Party imports
import arcade
# Project imports
from support import consts, utils


def launch_game(window):
    window.setup()
    arcade.play_sound(window.level_back_melody)


def relaunch_game(window):
    window.__init__()
    launch_game(window)


def pause_game(player_sprite):
    player_sprite.stop()
    arcade.draw_text(
        "OPTIONS",
        consts.SCREEN_WIDTH/2,
        consts.SCREEN_HEIGHT-200,
        arcade.color.RED,
        24,
        anchor_x="center",
        anchor_y="center"
    )
    time.pause()


def finish_game(
    player_sprite,
    score_text_position_x,
    score_text_position_y,
):
    utils.reset_viewport_position()
    player_sprite.center_y = 100
    player_sprite.center_x = 550
    player_sprite.stop()
    player_sprite.remove_from_sprite_lists()
    score_text_position_x = consts.SCREEN_WIDTH - 950
    score_text_position_y = consts.SCREEN_HEIGHT - 50
    arcade.draw_text(
        "GAME OVER, DUDE!",
        consts.SCREEN_WIDTH/2,
        consts.SCREEN_HEIGHT/2,
        arcade.color.RED,
        24,
        anchor_x="center",
        anchor_y="center"
    )
    arcade.draw_text(
        f'Press "{consts.RESTART_GAME_BUTTON}" to START over',
        consts.SCREEN_WIDTH/2,
        consts.SCREEN_HEIGHT/2-50,
        arcade.color.RED,
        16,
        anchor_x="center",
        anchor_y="center"
    )
    return True
