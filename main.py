# Python imports
from decouple import config
import random
# Django imports
# Third-Party imports
import arcade
# Project imports

x = float(1/60)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(
            int(config('SCREEN_WIDTH', 120)),
            int(config('SCREEN_HEIGHT', 120)),
            config('SCREEN_TITLE', 'Error in title')
        )

        # These are 'lists' that keep track of our sprites. Each sprite should go into a list.
        self.player_list = None
        self.coins_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.coin_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the character at specific coordinates.
        image_source = "images/player_1/r0.png"
        self.player_sprite = arcade.Sprite(
            image_source, float(config('SCALING', 1)))
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # Setup coins animated sprite
        for i in range(20):
            coin = arcade.AnimatedTimeSprite(x)
            coin.center_x = random.randint(
                50,
                int(config('SCREEN_WIDTH', 120))-50,
            )
            coin.center_y = random.randint(
                50,
                int(config('SCREEN_HEIGHT', 120))-50
            )
            coin.textures = []
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
            coin.scale = float(config('COIN_SCALING', 1))
            coin.cur_texture_index = random.randint(0, len(coin.textures))
            self.coin_list.append(coin)

    def on_update(self, delta_time):
        self.coin_list.update()
        self.coin_list.update_animation()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.player_list.draw()
        self.coin_list.draw()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
