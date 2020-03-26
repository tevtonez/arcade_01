# Python imports
import time
# Third-Party imports
import arcade
from decouple import config
# Project imports
from sprite_support.character import character_sprite
from sprite_support.coin import coin_sprite
from support import consts, utils


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
        self.coin_list = None
        self.wall_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.score_text_position_x = 0
        self.score_text_position_y = 0

        # coins counter (eg points)
        self.score = None

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sound/coins/coin_1.wav")
        self.jump_sound = arcade.load_sound("sound/player/jump_1.wav")
        self.scream_sound = arcade.load_sound('sound/player/fall_2.wav')
        self.level_back_melody = arcade.load_sound("sound/game/level_1.wav")
        self.win_sound = arcade.load_sound('sound/game/win_1.wav')
        self.lost_sound = arcade.load_sound('sound/game/lost_1.wav')

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.score = 0

        # Set up the character at specific coordinates.
        self.player_sprite, self.player_list = character_sprite.make_player_sprite(
            self.player_sprite,
            self.player_list
        )
        self.player_fell_sound_play = False
        self.player_died = False
        self.game_over = False
        self.draw_game_over = False
        self.play_win_sound = False
        self.show_help_menu = False

        # Setup coins animated sprite
        self.coin_list = coin_sprite.make_coin_sprite(self.coin_list)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1000, 53):
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
            [200, 430],
            [429, 400],
            [669, 425],
            [889, 413],
            [579, 202],
            [320, 550],
            [520, 540],
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
                self.player_sprite.change_y = consts.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
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

        if key == arcade.key.R:
            relaunch_game(self)

        if key == arcade.key.Q:
            quit()

        if key == arcade.key.ESCAPE and self.show_help_menu:
            self.show_help_menu = False
        elif key == arcade.key.ESCAPE and not self.show_help_menu:
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
            arcade.set_viewport(self.view_left,
                                consts.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                consts.SCREEN_HEIGHT + self.view_bottom)

            # text position
            self.score_text_position_x = consts.SCREEN_WIDTH + self.view_left - 950
            self.score_text_position_y = consts.SCREEN_HEIGHT + self.view_bottom - 50

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        arcade.draw_text(
            f"Coins: {self.score}/{consts.COIN_NUMBER}",
            self.score_text_position_x,
            self.score_text_position_y,
            arcade.color.WHITE,
            14,
        )

        if self.draw_game_over:
            self.player_sprite.center_y = 100
            self.player_sprite.center_x = 550
            self.player_sprite.stop()
            self.player_sprite.remove_from_sprite_lists()
            self.score_text_position_x = consts.SCREEN_WIDTH - 950
            self.score_text_position_y = consts.SCREEN_HEIGHT - 50
            arcade.set_viewport(
                0,
                consts.SCREEN_WIDTH,
                0,
                consts.SCREEN_HEIGHT
            )

            arcade.draw_text(
                "GAME OVER, DUDE!",
                consts.SCREEN_WIDTH/2,
                consts.SCREEN_HEIGHT/2,
                arcade.color.RED,
                24,
                anchor_x="center",
                anchor_y="center"
            )
            arcade.draw_text(
                f'Press "{consts.RESTART_GAME_BUTTON}" to START over',
                consts.SCREEN_WIDTH/2,
                consts.SCREEN_HEIGHT/2-50,
                arcade.color.RED,
                16,
                anchor_x="center",
                anchor_y="center"
            )

        if self.show_help_menu:
            arcade.set_viewport(
                0,
                consts.SCREEN_WIDTH,
                0,
                consts.SCREEN_HEIGHT
            )
            self.player_sprite.stop()
            arcade.draw_text(
                "OPTIONS",
                consts.SCREEN_WIDTH/2,
                consts.SCREEN_HEIGHT/2,
                arcade.color.RED,
                24,
                anchor_x="center",
                anchor_y="center"
            )
            time.pause()

        # Draw our sprites
        self.player_list.draw()
        self.coin_list.draw()
        self.wall_list.draw()


def launch_game():
    window = MyGame()
    window.setup()
    arcade.play_sound(window.level_back_melody)


def relaunch_game(window):
    window.__init__()
    window.setup()
    arcade.play_sound(window.level_back_melody)


def main():
    """ Main method """
    launch_game()
    arcade.run()


if __name__ == "__main__":
    main()
