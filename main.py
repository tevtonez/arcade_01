# Python imports
from decouple import config
# Django imports
# Third-Party imports
import arcade
# Project imports


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
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
