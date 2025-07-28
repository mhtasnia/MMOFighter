# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Frames per second
FPS = 60

# Physics
GRAVITY = 0.75

# Player properties
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = -25
PLAYER_HEALTH = 100
PLAYER_WIDTH = 200
PLAYER_HEIGHT = 200

# Attack properties
LIGHT_ATTACK_DAMAGE = 5
LIGHT_ATTACK_RANGE = 100
LIGHT_ATTACK_COOLDOWN = 300  # milliseconds

HEAVY_ATTACK_DAMAGE = 15
HEAVY_ATTACK_RANGE = 130
HEAVY_ATTACK_COOLDOWN = 800  # milliseconds

# Blocking properties
BLOCK_DAMAGE_REDUCTION = 0.5 # 50% damage reduction

# Power Meter properties
POWER_METER_MAX = 100
POWER_GAIN_ON_HIT = 10
POWER_GAIN_ON_RECEIVE_HIT = 5
SPECIAL_MOVE_COST = 50
SPECIAL_MOVE_DAMAGE = 40
SPECIAL_MOVE_RANGE = 150
SPECIAL_MOVE_COOLDOWN = 1000 # milliseconds

# Knockback properties
LIGHT_KNOCKBACK_STRENGTH = 5
HEAVY_KNOCKBACK_STRENGTH = 15
SPECIAL_KNOCKBACK_STRENGTH = 25

# Hit effect properties
HIT_EFFECT_DURATION = 100 # milliseconds

# Hit reaction properties
HIT_STUN_DURATION = 500 # milliseconds

# Combo properties
COMBO_WINDOW = 300 # milliseconds

# Attack effect properties
ATTACK_EFFECT_DURATION = 100 # milliseconds

# UI properties
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREY = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

# Buttons
BUTTON_COLOR = GREY # Added for consistency in button styling

# Font Sizes
GAME_OVER_FONT_SIZE = 72
TITLE_FONT_SIZE = 72
CONTROLS_FONT_SIZE = 20 # New: Smaller font size for controls

# Game States
GAME_STATE_MENU = "menu"
GAME_STATE_RUNNING = "running"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"