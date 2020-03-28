# Python imports
# Third-Party imports
import arcade
from decouple import config
# Project imports
from sprite_support.coin import coin_sprite
from support import(
    consts,
    utils,
    game_class_utils,
    game_control_utils,
)


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

        # initialize flags vars for window class instance
        game_class_utils.init_flags(self)

        # Load sounds
        game_class_utils.init_sounds(self)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Setup coins animated sprite
        self.coin_list = coin_sprite.make_coin_sprite(self.coin_list)

        # Setup game variables (flags)
        game_class_utils.setup_flags(self)

        # Create the ground and blocks
        utils.draw_ground_blocks(self)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            consts.GRAVITY
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        player_movement_speed = consts.PLAYER_MOVEMENT_SPEED
        if not self.block_keys or self.block_movement_keys:
            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = consts.PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -player_movement_speed
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = player_movement_speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.R:
            game_control_utils.relaunch_game(self)

        if key == arcade.key.Q:
            quit()

        if not self.block_keys:
            if not self.block_movement_keys:
                if key == arcade.key.LEFT or key == arcade.key.A:
                    self.player_sprite.change_x = 0
                elif key == arcade.key.RIGHT or key == arcade.key.D:
                    self.player_sprite.change_x = 0

            if key == arcade.key.ESCAPE and self.show_help_menu:
                self.block_movement_keys = False
                self.show_help_menu = False
            elif key == arcade.key.ESCAPE and not self.show_help_menu:
                self.block_movement_keys = True
                self.show_help_menu = True

    def on_update(self, delta_time):
        """ Movement and game logic """

        # update coins animation
        self.coin_list.update()
        self.coin_list.update_animation()

        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.coin_list
        )
        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # FINISH GAME IF FOUND ALL COINS!!!
        if self.score == consts.COIN_NUMBER and not self.play_win_sound:
            self.play_win_sound = True
            arcade.play_sound(self.win_sound)

        # Finish game if player fell
        if self.player_sprite.center_y < 90 and not self.player_died:
            self.game_over = True
            self.player_died = True
            self.player_fell_sound_play = True

        if self.player_fell_sound_play:
            self.player_fell_sound_play = False
            arcade.play_sound(self.scream_sound)

        # play game over
        if self.player_sprite.center_y < -4090 and self.game_over:
            self.game_over = False
            arcade.play_sound(self.lost_sound)
            self.draw_game_over = True

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        view_changed = False

        # Scroll left
        left_boundary = self.view_left + consts.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            view_changed = True

        # Scroll right
        right_boundary = self.view_left + consts.SCREEN_WIDTH - consts.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            view_changed = True

        # Scroll up
        top_boundary = self.view_bottom + consts.SCREEN_HEIGHT - consts.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            view_changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + consts.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            view_changed = True

        if view_changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(
                self.view_left,
                consts.SCREEN_WIDTH + self.view_left,
                self.view_bottom,
                consts.SCREEN_HEIGHT + self.view_bottom
            )

            # text position
            self.score_text_position_x, self.score_text_position_y = utils.calculate_score_position(
                self.view_left,
                self.view_bottom,
            )

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        utils.draw_score(
            self.score,
            self.score_text_position_x,
            self.score_text_position_y,
        )

        utils.draw_esc_hint(
            self.score_text_position_x,
            self.score_text_position_y,
        )

        if self.draw_game_over:
            self.block_keys = game_control_utils.finish_game(
                self.player_sprite,
                self.score_text_position_x,
                self.score_text_position_y,
            )

        if self.show_help_menu:
            game_control_utils.pause_game(self.player_sprite)

        # Draw our sprites
        self.player_list.draw()
        self.coin_list.draw()
        self.wall_list.draw()


def main():
    """ Main method """
    window = MyGame()
    game_control_utils.launch_game(window)
    arcade.run()


if __name__ == "__main__":
    main()
