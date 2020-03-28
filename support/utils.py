# Python imports
# Third-Party imports
import arcade
# Project imports
from support import consts


def reset_viewport_position():
    arcade.set_viewport(
        0,
        consts.SCREEN_WIDTH,
        0,
        consts.SCREEN_HEIGHT
    )


def draw_score(
    score,
    score_text_position_x,
    score_text_position_y,
):
    arcade.draw_text(
        f"Coins: {score}/{consts.COIN_NUMBER}",
        score_text_position_x,
        score_text_position_y,
        arcade.color.WHITE,
        14,
    )


def draw_esc_hint(
    score_text_position_x,
    score_text_position_y,
):
    arcade.draw_text(
        "Press [ESC] for menu",
        score_text_position_x + consts.SCREEN_WIDTH - 220,
        score_text_position_y,
        arcade.color.WHITE,
        12,
    )


def draw_ground_blocks(window_instance):
    # Place multiple block sprites horizontally
    for x in range(0, 1000, 52):
        wall = arcade.Sprite(
            "images/tiles/ground/tile_ground.png",
            consts.TILE_SCALING
        )
        wall.center_x = x
        wall.center_y = 32
        window_instance.wall_list.append(wall)

    # Blocks in the air
    for coordinate in consts.BLOCKS_COORDINATES:
        # Add a crate on the ground
        platform = arcade.Sprite(
            "images/tiles/ground/tile_ground.png",
            consts.TILE_SCALING
        )
        platform.position = coordinate
        window_instance.wall_list.append(platform)


def calculate_score_position(view_left, view_bottom):
    score_text_position_x = consts.SCREEN_WIDTH + view_left - 950
    score_text_position_y = consts.SCREEN_HEIGHT + view_bottom - 50
    return score_text_position_x, score_text_position_y
