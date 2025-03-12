import arcade

# --- CONSTANTS ---
# Screen
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Hell Jumper"

# Player
SPRITE_SCALING_JUMPER = 2
JUMP_STRENGTH = 7.5 # Up movement by player on keystroke, in pixels
GRAVITY = 0.5

# Obstacles
SPRITE_SCALING_BARRIER = 1

class Jumper(arcade.Sprite):
    """Jumper (Player) Class"""

    def __init__(self, texture_path, scale, start_x, start_y):
        """Initialize the jumper"""
        super().__init__(texture_path, scale)

        # Set initial position
        self.center_x = start_x
        self.center_y = start_y

        # Velocity attributes
        self.change_y = 0

    def update(self, delta_time: float = 1/60):
        """Move Jumper"""

        # Apply gravity
        self.change_y -= GRAVITY

        # Apply Movement
        self.center_y += self.change_y
    
    def jump(self):
        """Handles jump behaviors"""
        self.change_y = JUMP_STRENGTH

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
        self.obstacle_list = None

        # Set up jumper info
        self.jumper_sprite = None
        self.score = 0

        self.background_color = (33, 37, 43, 255)

    def setup(self):
        """Set up the game and initialize variables. Called to restart the game."""
        
        # Sprite lists
        self.jumper_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the jumper
        self.jumper_sprite = Jumper("assets/jumper/0.png", SPRITE_SCALING_JUMPER, 100, 325)
        self.jumper_list.append(self.jumper_sprite)

    def on_draw(self):
        """ Render the screen. """

        self.clear()
        
        # Draw sprites
        self.jumper_list.draw()
    
    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Move the player
        self.jumper_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        """Called whenever jump key is pressed"""

        if key == arcade.key.UP:
            self.jumper_sprite.jump()

def main():
    """Main function"""
    game = HellJumperGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
