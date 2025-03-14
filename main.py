import arcade
import random

# --- CONSTANTS ---
# Screen
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
WINDOW_TITLE = "HELLJUMPER"

# Game States
START_SCREEN = 0
PLAYING = 1
GAME_OVER = 2

# Player
SPRITE_SCALING_JUMPER = .3
JUMPER_START_X = 250
JUMPER_START_Y = 450
JUMP_STRENGTH = 7.5 # Up movement by player on keystroke
GRAVITY = 0.5 # Down movement by player (constantly when no keystroke)

# Obstacles
SPRITE_SCALING_BARRIER = 1
BARRIER_WIDTH = 150
BARRIER_HEIGHT = 450
BARRIER_GAP = 200  # Vertical gap between top and bottom barriers
BARRIER_INTERVAL = 300 # Horizontal gap between barriers
BARRIER_BASE_SPEED = 5  # Speed at which barriers move left
BARRIER_SPEED_INCREASE = 0.1  # Speed at which barriers move left

class Jumper(arcade.Sprite):
    """Jumper (Player) Class"""

    def __init__(self, texture_path, scale, start_x, start_y):
        """Initialize the jumper"""
        super().__init__(texture_path, scale, start_x, start_y)

        # Set initial position
        self.center_x = start_x
        self.center_y = start_y

        # Velocity attributes
        self.change_y = 0

    def update(self, delta_time: float = 1/60):
        """Move Jumper"""

        # Apply gravity
        self.change_y -= GRAVITY
        # self.angle += 0.35 # OPTIONAL ROTATION
        # if self.angle > 359:
        #     self.angle -= 360

        # Apply Movement
        self.center_y += self.change_y
    
    def jump(self):
        """Handles jump behaviors"""
        
        # Set up jumps sound
        self.jump_sound = arcade.load_sound("assets/jumpSound.wav")
        
        self.change_y = JUMP_STRENGTH
        arcade.play_sound(self.jump_sound, volume=1, loop=False)
        

class Barrier(arcade.Sprite):
    """Barrier Class"""
    def __init__(self, texture_path, scale, x, y, width, height):
        """Initialize the barrier"""
        super().__init__(texture_path, scale)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
    
    def update(self, delta_time: float = 1/60):
        """Move the barrier"""
        self.center_x -= BARRIER_SPEED

        # Remove the barrier when it moves off-screen
        if self.center_x + self.width < 0:
            self.kill()

class HellJumperGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer
        """

        # Setting up the game window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        # Current game state
        self.game_state = START_SCREEN # Initializes in start screen
        self.score = 0
        
        # Variables for sprite lists
        self.jumper_list = None
        self.barrier_list = None

        # Set up jumper info
        self.jumper_sprite = None

        # Set up background image
        self.background_list = None

        self.background_color = (33, 37, 43, 255)

        # Set up background music variables
        self.background_music = arcade.load_sound("assets/backgroundMusic.mp3")
        arcade.play_sound(self.background_music, volume=0.01, loop=True)

    def setup(self):
        """Set up the game and initialize variables. Called to restart the game."""

        self.set_mouse_visible(False)
        
        # Reset to start game state
        self.score = 0

        # Sprite lists
        self.background_list = arcade.SpriteList()
        self.jumper_list = arcade.SpriteList()
        self.barrier_list = arcade.SpriteList()

        self.background_sprite = arcade.Sprite("assets/terrain/background3.png")
        self.background_sprite.center_x = WINDOW_WIDTH // 2
        self.background_sprite.center_y = WINDOW_HEIGHT // 2
        self.background_list.append(self.background_sprite)

        # Set up the jumper
        self.jumper_sprite = Jumper("assets/jumper/jumper1.png", SPRITE_SCALING_JUMPER, JUMPER_START_X, JUMPER_START_Y)
        self.jumper_list.append(self.jumper_sprite)

        # Spwan the first few barriers
        self.spawn_barrier()

    def on_draw(self):
        """ Render the screen. """

        self.clear()
        
        # Draw sprites
        self.background_list.draw()
        self.jumper_list.draw()
        self.barrier_list.draw()

        # Draw overlay if in START_SCREEN or GAME_OVER state
        if self.game_state in (START_SCREEN, GAME_OVER):

            self.set_mouse_visible(True)
            
            if self.game_state == START_SCREEN:
                message = "HELLJUMPER"
            else:
                message = "MISSION FAILED"

            arcade.draw_lrbt_rectangle_filled(5, 595, 250, 410, (0, 0, 0, 155))

            arcade.draw_text(message, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                             arcade.color.WHITE, 64, bold=True, anchor_x="center")
            arcade.draw_text("Press <SPACE> to start", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50,
                             arcade.color.WHITE, 32, anchor_x="center")
        
        # Draw score count
        arcade.draw_text(self.score // 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60,
                             arcade.color.WHITE, 48, bold=True, anchor_x="center")
    
    def on_update(self, delta_time):
        """Update game state if playing."""

        if self.game_state != PLAYING:
            return
        
        # Dynamic barrier speed adjustment
        global BARRIER_SPEED
        BARRIER_SPEED = BARRIER_BASE_SPEED + (self.score // 2) * BARRIER_SPEED_INCREASE

        # Move the player and barriers
        self.jumper_list.update(delta_time)
        self.barrier_list.update()

        # Spawn new barriers
        if len(self.barrier_list) == 0 or self.barrier_list[-1].center_x < WINDOW_WIDTH - BARRIER_INTERVAL:
            self.spawn_barrier()

        # Increase the score as long as the jumper is passing barriers
        for barrier in self.barrier_list:
            if barrier.center_x + BARRIER_WIDTH < self.jumper_sprite.center_x and not hasattr(barrier, "scored"):
                self.score += 1
                barrier.scored = True  # Mark barrier as scored to avoid multiple counts
        
        # Check for collisions with barriers or top/bottom
        if arcade.check_for_collision_with_list(self.jumper_sprite, self.barrier_list) or self.jumper_sprite.bottom < 0 or self.jumper_sprite.top > WINDOW_HEIGHT:
            self.game_over()

    def on_key_press(self, key, modifiers):
        """Handles jump key presses"""

        if key == arcade.key.SPACE or key == arcade.key.UP:
            if self.game_state in (START_SCREEN, GAME_OVER):
                self.game_state = PLAYING
                self.setup()
            else:
                self.jumper_sprite.jump()
                # self.jumper_sprite.angle -= 8.75 # OPTIONAL ROTATION

    def on_mouse_press(self, x, y, button, modifiers): 
        """Handles mouse-click for jump"""

        if self.game_state in (START_SCREEN, GAME_OVER):
            self.game_state = PLAYING
            self.setup()
        else:
            self.jumper_sprite.jump()


    def spawn_barrier(self):
        """Spawns a new barrier with a random gap position"""

        # Generate random y-offset for bottom barrier
        random_y_offset = random.randrange(-200, 200, 10)
        
        # Create top and bottom barriers
        bottom_barrier = Barrier(
            "assets/terrain/barrier_bottom.png",
            SPRITE_SCALING_BARRIER, 
            WINDOW_WIDTH + BARRIER_WIDTH, 
            random_y_offset, 
            BARRIER_WIDTH, 
            BARRIER_HEIGHT
            )
        top_barrier = Barrier(
            "assets/terrain/barrier_top.png", 
            SPRITE_SCALING_BARRIER, 
            WINDOW_WIDTH + BARRIER_WIDTH, 
            bottom_barrier.center_y + BARRIER_GAP + BARRIER_HEIGHT, 
            BARRIER_WIDTH, 
            BARRIER_HEIGHT)

        self.barrier_list.append(bottom_barrier)
        self.barrier_list.append(top_barrier)
    
    def game_over(self):
        """Handles game over state"""
        print("Game Over!")  # Replace this with your game over logic
        self.game_state = GAME_OVER


def main():
    """Main function"""
    game = HellJumperGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
