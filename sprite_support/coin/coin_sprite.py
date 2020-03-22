# Python imports
import random
# Third-Party imports
import arcade
from decouple import config
# Project imports


def make_coin_sprite(coin_list):
    for i in range(int(config('COIN_NUMBER', 20))):
        coin = arcade.AnimatedTimeSprite()
        coin.center_x = random.randint(
            50,
            int(config('SCREEN_WIDTH', 120))-50,
        )
        coin.center_y = random.randint(
            150,
            int(config('SCREEN_HEIGHT', 120))-50
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
        coin.scale = float(config('COIN_SCALING', 1))
        coin.cur_texture_index = random.randint(2, len(coin.textures)-2)
        coin_list.append(coin)
