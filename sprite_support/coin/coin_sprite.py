# Python imports
import random
# Third-Party imports
import arcade
from support import consts
# Project imports


def make_coin_sprite(coin_list):
    for i in range(consts.COIN_NUMBER):
        coin = arcade.AnimatedTimeSprite()
        coin.center_x = random.randint(
            50,
            consts.SCREEN_WIDTH-50,
        )
        coin.center_y = random.randint(
            150,
            consts.SCREEN_HEIGHT-50
        )
        coin.textures = []
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_1.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_1.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_1.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_2.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_3.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_4.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_5.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_6.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_1.png"))
        coin.textures.append(arcade.load_texture(
            "images/coin/coin_1.png"))
        coin.scale = consts.COIN_SCALING
        coin.cur_texture_index = random.randint(2, len(coin.textures)-2)
        coin_list.append(coin)

    return coin_list
