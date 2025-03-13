import arcade
import random

# --- CONSTANTS ---
# Screen
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Hell Jumper"

# Player
SPRITE_SCALING_JUMPER = 1
JUMPER_START_X = 100
JUMPER_START_Y = 550
JUMP_STRENGTH = 7.5 # Up movement by player on keystroke
GRAVITY = 0.5 # Down movement by player (constantly when no keystroke)

# Obstacles
SPRITE_SCALING_BARRIER = 1
BARRIER_WIDTH = 50
BARRIER_HEIGHT = 450
BARRIER_GAP = 200  # Vertical gap between top and bottom barriers
BARRIER_INTERVAL = 150 # Horizontal gap between barriers
BARRIER_SPEED = 2  # Speed at which barriers move leftward

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
        self.change_y = JUMP_STRENGTH

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
        
        # Variables for sprite lists
        self.jumper_list = None
        self.barrier_list = None

        # Set up jumper info
        self.jumper_sprite = None
        self.score = 0

        self.background_color = (33, 37, 43, 255)

        # Interval distance for barriers
        self.barrier_interval = 100

    def setup(self):
        """Set up the game and initialize variables. Called to restart the game."""
        
        # Sprite lists
        self.jumper_list = arcade.SpriteList()
        self.barrier_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the jumper
        self.jumper_sprite = Jumper("assets/jumper/0.png", SPRITE_SCALING_JUMPER, JUMPER_START_X, JUMPER_START_Y)
        self.jumper_list.append(self.jumper_sprite)

        # Spwan the first few barriers
        self.spawn_barrier()

    def on_draw(self):
        """ Render the screen. """

        self.clear()
        
        # Draw sprites
        self.jumper_list.draw()
        self.barrier_list.draw()
    
    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Move the player and barriers
        self.jumper_list.update(delta_time)
        self.barrier_list.update()

        # Spawn new barriers
        if len(self.barrier_list) == 0 or self.barrier_list[-1].center_x < WINDOW_WIDTH - BARRIER_INTERVAL:
            self.spawn_barrier()
        
        # Check for collisions with barriers or top/bottom
        if arcade.check_for_collision_with_list(self.jumper_sprite, self.barrier_list):
            self.game_over()
        elif self.jumper_sprite.bottom < 0:
            self.game_over()
        elif self.jumper_sprite.top > 650:
            self.game_over()

    def on_key_press(self, key, modifiers):
        """Called whenever jump key is pressed"""

        if key == arcade.key.SPACE:
            self.jumper_sprite.jump()
            # self.jumper_sprite.angle -= 8.75 # OPTIONAL ROTATION


    def spawn_barrier(self):
        """Spawns a new barrier with a random gap position"""

        # Generate random y-offset for bottom barrier
        random_y_offset = random.randrange(-200, 200, 10)
        
        # Create top and bottom barriers
        bottom_barrier = Barrier(
            "assets/terrain/1.png",
            SPRITE_SCALING_BARRIER, 
            WINDOW_WIDTH + BARRIER_WIDTH, 
            random_y_offset, 
            BARRIER_WIDTH, 
            BARRIER_HEIGHT
            )
        top_barrier = Barrier(
            "assets/terrain/2.png", 
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
        self.setup()


def main():
    """Main function"""
    game = HellJumperGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
