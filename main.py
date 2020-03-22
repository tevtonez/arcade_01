# Python imports
# Third-Party imports
import arcade
from decouple import config
# Project imports
from sprites.character import character_sprite
from sprites.coin import coin_sprite

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
        self.wall_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the character at specific coordinates.
        character_sprite.make_player_sprite(
            self.player_sprite, self.player_list)

        # Setup coins animated sprite
        coin_sprite.make_coin_sprite(self.coin_list)

        # Walls sprite will be added here

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
        self.wall_list.draw()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
