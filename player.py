
import pygame
from settings import *

class Player:
    def __init__(self, x, y, image_path, attack_sound, block_sound, jump_sound):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.health = PLAYER_HEALTH
        self.is_attacking = False
        self.attack_cooldown = 0
        self.hitbox = None
        self.hit_stun_timer = 0
        self.is_blocking = False
        self.power_meter = 0
        self.special_move_cooldown = 0
        self.hit_effect_timer = 0
        self.combo_timer = 0
        self.combo_count = 0
        self.attack_effect_timer = 0

        # Sound effects
        self.attack_sound = attack_sound
        self.block_sound = block_sound
        self.jump_sound = jump_sound

        # Image handling
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.direction = 1 # 1 for right, -1 for left
        self.frame_rate = 250 # milliseconds per frame

    def set_blocking(self, blocking):
        self.is_blocking = blocking
        if blocking:
            self.block_sound.play()

    def gain_power(self, amount):
        self.power_meter += amount
        if self.power_meter > POWER_METER_MAX:
            self.power_meter = POWER_METER_MAX

    def move(self, direction):
        if self.hit_stun_timer == 0 and not self.is_blocking:
            self.velocity.x = direction * PLAYER_SPEED
            if direction != 0:
                self.direction = direction

    def jump(self):
        if self.on_ground and self.hit_stun_timer == 0 and not self.is_blocking:
            self.velocity.y = PLAYER_JUMP_STRENGTH
            self.jump_sound.play()

    def attack(self, damage, attack_range, cooldown, knockback_strength):
        if self.attack_cooldown == 0 and self.hit_stun_timer == 0 and not self.is_blocking:
            self.is_attacking = True
            self.attack_cooldown = cooldown
            self.attack_effect_timer = ATTACK_EFFECT_DURATION # Start attack effect
            self.attack_sound.play()
            hitbox_x = self.rect.centerx + (self.direction * (self.rect.width // 2))
            self.hitbox = pygame.Rect(hitbox_x, self.rect.y, attack_range, self.rect.height)
            self.current_attack_damage = damage
            self.current_knockback_strength = knockback_strength

    def special_move(self):
        if self.power_meter >= SPECIAL_MOVE_COST and self.special_move_cooldown == 0 and self.hit_stun_timer == 0 and not self.is_blocking:
            self.power_meter -= SPECIAL_MOVE_COST
            self.is_attacking = True
            self.special_move_cooldown = SPECIAL_MOVE_COOLDOWN
            self.attack_cooldown = SPECIAL_MOVE_COOLDOWN # Use special move cooldown for attack cooldown
            self.attack_effect_timer = ATTACK_EFFECT_DURATION # Start attack effect
            self.attack_sound.play()
            hitbox_x = self.rect.centerx + (self.direction * (self.rect.width // 2))
            self.hitbox = pygame.Rect(hitbox_x - (SPECIAL_MOVE_RANGE // 2), self.rect.y, SPECIAL_MOVE_RANGE, self.rect.height)
            self.current_attack_damage = SPECIAL_MOVE_DAMAGE
            self.current_knockback_strength = SPECIAL_KNOCKBACK_STRENGTH

    def update(self, opponent):
        # Handle hit stun
        if self.hit_stun_timer > 0:
            self.hit_stun_timer -= self.frame_rate # Decrement by frame rate for simplicity
            if self.hit_stun_timer < 0:
                self.hit_stun_timer = 0
            self.velocity.x = 0 # Stop movement during hit stun

        # Handle special move cooldown
        if self.special_move_cooldown > 0:
            self.special_move_cooldown -= self.frame_rate
            if self.special_move_cooldown < 0:
                self.special_move_cooldown = 0

        # Handle hit effect
        if self.hit_effect_timer > 0:
            self.hit_effect_timer -= self.frame_rate
            if self.hit_effect_timer < 0:
                self.hit_effect_timer = 0

        # Handle attack effect
        if self.attack_effect_timer > 0:
            self.attack_effect_timer -= self.frame_rate
            if self.attack_effect_timer < 0:
                self.attack_effect_timer = 0

        # Handle combo timer
        if self.combo_timer > 0:
            self.combo_timer -= self.frame_rate
            if self.combo_timer < 0:
                self.combo_timer = 0
                self.combo_count = 0 # Reset combo if timer expires

        # Apply gravity
        self.velocity.y += GRAVITY
        self.rect.y += self.velocity.y

        # Move horizontally
        self.rect.x += self.velocity.x

        # Boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Check for ground collision
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= self.frame_rate # Decrement by frame rate
            if self.attack_cooldown < 0:
                self.attack_cooldown = 0

        # Reset attack state
        if self.is_attacking and self.attack_cooldown == 0:
            self.is_attacking = False
            self.hitbox = None

        # Check for attack collision
        if self.hitbox and self.hitbox.colliderect(opponent.rect):
            damage_to_deal = self.current_attack_damage
            if opponent.is_blocking:
                damage_to_deal *= BLOCK_DAMAGE_REDUCTION
            opponent.health -= damage_to_deal
            opponent.hit_stun_timer = HIT_STUN_DURATION # Apply hit stun
            opponent.velocity.x += self.current_knockback_strength * self.direction # Apply knockback
            opponent.hit_effect_timer = HIT_EFFECT_DURATION # Apply hit effect
            opponent.gain_power(POWER_GAIN_ON_RECEIVE_HIT)
            self.gain_power(POWER_GAIN_ON_HIT)

            # Combo logic
            if self.combo_timer > 0:
                self.combo_count += 1
            else:
                self.combo_count = 1
            self.combo_timer = COMBO_WINDOW # Reset combo timer

            self.hitbox = None # Prevent multiple hits

    def draw(self, surface):
        # Flash red when in hit stun
        if self.hit_stun_timer > 0 and (pygame.time.get_ticks() // 100) % 2 == 0:
            temp_image = self.image.copy()
            temp_image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            image_to_draw = pygame.transform.flip(temp_image, self.direction == -1, False)
        elif self.is_blocking:
            temp_image = self.image.copy()
            temp_image.fill((0, 0, 255, 128), special_flags=pygame.BLEND_RGBA_MULT) # Blue tint for blocking
            image_to_draw = pygame.transform.flip(temp_image, self.direction == -1, False)
        else:
            image_to_draw = pygame.transform.flip(self.image, self.direction == -1, False)

        # Draw attack effect
        if self.attack_effect_timer > 0:
            attack_effect_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            attack_effect_surface.fill((255, 255, 0, 50)) # Yellow transparent overlay
            image_to_draw.blit(attack_effect_surface, (0, 0))

        # Draw hit effect
        if self.hit_effect_timer > 0:
            hit_effect_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            hit_effect_surface.fill((255, 255, 255, 100)) # White transparent overlay
            image_to_draw.blit(hit_effect_surface, (0, 0))

        surface.blit(image_to_draw, self.rect)



        
