# Python imports
from decouple import config
# Django imports
# Third-Party imports
import arcade
# Project imports

# Set constants for the screen size
screen_width = int(config('SCREEN_WIDTH'))
screen_height = int(config('SCREEN_HEIGHT'))

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(screen_width, screen_height, "Drawing Example")


# Set the background color to white.
# For a list of named colors see:
# http://arcade.academy/arcade.color.html
# Colors can also be specified in (red, green, blue) format and
# (red, green, blue, alpha) format.
arcade.set_background_color(arcade.color.WHITE)

# Start the render process. This must be done before any drawing commands.
arcade.start_render()

arcade.draw_text("draw_bitmap", 483, 3, arcade.color.BLACK, 12)

# Finish drawing and display the result
arcade.finish_render()


# Keep the window open until the user hits the 'close' button
arcade.run()
