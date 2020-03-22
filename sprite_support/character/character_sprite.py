# Python imports
# Third-Party imports
import arcade
from decouple import config
# Project imports


def make_player_sprite(player_sprite, player_list):
    image_source = "images/player_1/r0.png"
    player_sprite = arcade.Sprite(
        image_source,
        float(config('SCALING', 1))
    )
    player_sprite.center_x = 20
    player_sprite.center_y = 96
    player_list.append(player_sprite)
