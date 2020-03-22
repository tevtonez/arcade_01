# Python imports
# Third-Party imports
import arcade
from decouple import config
# Project imports
from sprite_support.character import character_sprite
from sprite_support.coin import coin_sprite
from support import consts


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(
            consts.SCREEN_WIDTH,
            consts.SCREEN_HEIGHT,
            consts.SCREEN_TITLE
        )

        # These are 'lists' that keep track of our sprites. Each sprite should go into a list.
        self.player_list = None
        self.coins_list = None
        self.wall_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the character at specific coordinates.
        self.player_sprite, self.player_list = character_sprite.make_player_sprite(
            self.player_sprite,
            self.player_list
        )

        # Setup coins animated sprite
        self.coin_list = coin_sprite.make_coin_sprite(self.coin_list)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1650, 53):
            wall = arcade.Sprite(
                "images/tiles/ground/tile_ground.png",
                consts.TILE_SCALING
            )
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Walls sprite will be added here
        coordinate_list = [
            [512, 96],
            [256, 96],
            [768, 96],
            [132, 202],
            [429, 400],
            [579, 202],
        ]
        for coordinate in coordinate_list:
            # Add a crate on the ground
            platform = arcade.Sprite(
                "images/tiles/ground/tile_ground.png",
                consts.TILE_SCALING
            )
            platform.position = coordinate
            self.wall_list.append(platform)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            consts.GRAVITY
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        player_movement_speed = consts.PLAYER_MOVEMENT_SPEED
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = float(
                    config('PLAYER_JUMP_SPEED', 20))
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -player_movement_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = player_movement_speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # update coins animation
        self.coin_list.update()
        self.coin_list.update_animation()

        # Move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_boundary = self.view_left + consts.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + consts.SCREEN_WIDTH - consts.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + consts.SCREEN_HEIGHT - consts.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + consts.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                consts.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                consts.SCREEN_HEIGHT + self.view_bottom)

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
