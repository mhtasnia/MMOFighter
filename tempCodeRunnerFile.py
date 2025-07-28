import pygame

import sys
from settings import *
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.ATTACK_SOUND = pygame.mixer.Sound('assets/sounds/attack.mp3')
        self.BLOCK_SOUND = pygame.mixer.Sound('assets/sounds/block.mp3')
        self.JUMP_SOUND = pygame.mixer.Sound('assets/sounds/jump.mp3')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Corrected: Added image_path and used self. for sound objects
        self.player = Player(100, 100, "assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/characters/battleground.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        # Corrected: Used self. for sound objects
        self.player1 = Player(100, 200, "assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.player2 = Player(700, 200, "assets/characters/character2.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)

        self.font = pygame.font.SysFont("Arial", 30) # Using a system font for general text
        self.controls_font = pygame.font.SysFont("Arial", CONTROLS_FONT_SIZE)
        self.title_font = pygame.font.SysFont("Arial", TITLE_FONT_SIZE, bold=True) # For main menu title
        self.game_over_font = pygame.font.SysFont("Arial", GAME_OVER_FONT_SIZE, bold=True) # For game over text
        self.game_state = GAME_STATE_MENU # Start in menu state
        self.paused = False # New flag for pause state

        # Load and play background music
        pygame.mixer.music.load("assets/sounds/background-music-happy-375038.mp3")
        pygame.mixer.music.play(-1) # -1 means loop indefinitely


    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, x, y, width, height, inactive_color, active_color, text_color, action=None):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, active_color, button_rect, border_radius=10)
            if click[0] == 1 and action is not None:
                pygame.time.delay(200) # To prevent multiple clicks
                action()
        else:
            pygame.draw.rect(self.screen, inactive_color, button_rect, border_radius=10)

        self.draw_text(text, x, y, text_color, font=self.font)
        return button_rect # Return button_rect for external use if needed

    def draw_health_bar(self, player, x, y):
        ratio = player.health / PLAYER_HEALTH
        pygame.draw.rect(self.screen, RED, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.screen, GREEN, (x, y, HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))

    def draw_player_names_and_health(self):
        # Player 1 Name and Health Bar
        self.draw_text("Player 1", 20 + HEALTH_BAR_WIDTH // 2, 10, DARK_GREEN)
        self.draw_health_bar(self.player1, 20, 20)

        self.draw_text("VS", WIDTH // 2, 30, WHITE)

        # Player 2 Name and Health Bar
        self.draw_text("Player 2", WIDTH - HEALTH_BAR_WIDTH // 2 - 20, 10, DARK_GREEN)
        self.draw_health_bar(self.player2, WIDTH - HEALTH_BAR_WIDTH - 20, 20)

    def draw_power_meter(self, player, x, y):
        ratio = player.power_meter / POWER_METER_MAX
        pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.screen, BLUE, (x, y, HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))

    def reset_game(self):
        # Corrected: Added image_path and sound arguments
        self.player1 = Player(100, 200, "assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.player2 = Player(700, 200, "assets/characters/character2.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.game_state = GAME_STATE_RUNNING
        self.paused = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: # Pause button
                        if self.game_state == GAME_STATE_RUNNING:
                            self.game_state = GAME_STATE_PAUSED
                        elif self.game_state == GAME_STATE_PAUSED:
                            self.game_state = GAME_STATE_RUNNING

                if self.game_state == GAME_STATE_MENU:
                    # No direct mouse button down check here, handled by draw_button
                    pass

                elif self.game_state == GAME_STATE_RUNNING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.player1.set_blocking(True)

                        if event.key == pygame.K_DOWN:
                            self.player2.set_blocking(True)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_s:
                            self.player1.set_blocking(False)
                        if event.key == pygame.K_DOWN:
                            self.player2.set_blocking(False)

                elif self.game_state == GAME_STATE_GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()

            self.screen.blit(self.background, (0, 0)) # Draw background first

            if self.game_state == GAME_STATE_MENU:
                self.draw_text("MMO FIGHTER", WIDTH // 2, HEIGHT // 4, WHITE, font=self.title_font)

                # New Game Button
                self.draw_button("New Game", WIDTH // 2, HEIGHT // 2 - 50, 200, 60, BUTTON_COLOR, DARK_GREEN, WHITE, self.reset_game)

                # Quit Button
                self.draw_button("Quit", WIDTH // 2, HEIGHT // 2 + 30, 200, 60, BUTTON_COLOR, RED, WHITE, self.quit_game)

                # Controls
                # Player 1 Controls (Left Side)
                self.draw_text("Player 1 Controls:", WIDTH // 4, HEIGHT - 180, WHITE, font=self.controls_font)
                self.draw_text("Move: A/D", WIDTH // 4, HEIGHT - 150, WHITE, font=self.controls_font)
                self.draw_text("Jump: W", WIDTH // 4, HEIGHT - 130, WHITE, font=self.controls_font)
                self.draw_text("Light Attack: F", WIDTH // 4, HEIGHT - 110, WHITE, font=self.controls_font)
                self.draw_text("Heavy Attack: G", WIDTH // 4, HEIGHT - 90, WHITE, font=self.controls_font)
                self.draw_text("Special Move: H", WIDTH // 4, HEIGHT - 70, WHITE, font=self.controls_font)
                self.draw_text("Block: S", WIDTH // 4, HEIGHT - 50, WHITE, font=self.controls_font)

                # Player 2 Controls (Right Side)
                self.draw_text("Player 2 Controls:", WIDTH * 3 // 4, HEIGHT - 180, WHITE, font=self.controls_font)
                self.draw_text("Move: Left/Right Arrow", WIDTH * 3 // 4, HEIGHT - 150, WHITE, font=self.controls_font)
                self.draw_text("Jump: Up Arrow", WIDTH * 3 // 4, HEIGHT - 130, WHITE, font=self.controls_font)
                self.draw_text("Light Attack: RCtrl", WIDTH * 3 // 4, HEIGHT - 110, WHITE, font=self.controls_font)
                self.draw_text("Heavy Attack: RShift", WIDTH * 3 // 4, HEIGHT - 90, WHITE, font=self.controls_font)
                self.draw_text("Special Move: / (Slash)", WIDTH * 3 // 4, HEIGHT - 70, WHITE, font=self.controls_font)
                self.draw_text("Block: Down Arrow", WIDTH * 3 // 4, HEIGHT - 50, WHITE, font=self.controls_font)

            elif self.game_state == GAME_STATE_RUNNING:
                # Player 1 controls
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.player1.move(-1)
                elif keys[pygame.K_d]:
                    self.player1.move(1)
                else:
                    self.player1.move(0)

                if keys[pygame.K_w]:
                    self.player1.jump()

                if keys[pygame.K_UP]:
                    self.player2.jump()

                # Player 2 controls
                if keys[pygame.K_LEFT]:
                    self.player2.move(-1)
                elif keys[pygame.K_RIGHT]:
                    self.player2.move(1)
                else:
                    self.player2.move(0)

                if keys[pygame.K_f]:
                    self.player1.attack(LIGHT_ATTACK_DAMAGE, LIGHT_ATTACK_RANGE, LIGHT_ATTACK_COOLDOWN, LIGHT_KNOCKBACK_STRENGTH)
                if keys[pygame.K_g]:
                    self.player1.attack(HEAVY_ATTACK_DAMAGE, HEAVY_ATTACK_RANGE, HEAVY_ATTACK_COOLDOWN, HEAVY_KNOCKBACK_STRENGTH)
                if keys[pygame.K_h]:
                    self.player1.special_move()

                if keys[pygame.K_RCTRL]:
                    self.player2.attack(LIGHT_ATTACK_DAMAGE, LIGHT_ATTACK_RANGE, LIGHT_ATTACK_COOLDOWN, LIGHT_KNOCKBACK_STRENGTH)
                if keys[pygame.K_RSHIFT]:
                    self.player2.attack(HEAVY_ATTACK_DAMAGE, HEAVY_ATTACK_RANGE, HEAVY_ATTACK_COOLDOWN, HEAVY_KNOCKBACK_STRENGTH)
                if keys[pygame.K_SLASH]:
                    self.player2.special_move()

                # Update players
                self.player1.update(self.player2)
                self.player2.update(self.player1)

                # Check for game over
                if self.player1.health <= 0:
                    self.game_state = GAME_STATE_GAME_OVER
                    self.winner = "Player 2"
                elif self.player2.health <= 0:
                    self.game_state = GAME_STATE_GAME_OVER
                    self.winner = "Player 1"

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)

                # Draw health bars and names
                self.draw_player_names_and_health()

                # Draw power meters
                self.draw_power_meter(self.player1, 20, 50)
                self.draw_power_meter(self.player2, WIDTH - HEALTH_BAR_WIDTH - 20, 50)

                # Draw combo count
                if self.player1.combo_count > 0:
                    self.draw_text(f"P1 Combo: {self.player1.combo_count}", 100, 80, WHITE)
                if self.player2.combo_count > 0:
                    self.draw_text(f"P2 Combo: {self.player2.combo_count}", WIDTH - 100, 80, WHITE)

            elif self.game_state == GAME_STATE_PAUSED:
                # Draw a semi-transparent overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128)) # Black with 128 alpha (half transparent)
                self.screen.blit(overlay, (0, 0))
                self.draw_text("PAUSED", WIDTH // 2, HEIGHT // 2, WHITE, font=self.game_over_font)
                self.draw_text("Press 'P' to Resume", WIDTH // 2, HEIGHT // 2 + 70, WHITE)


            elif self.game_state == GAME_STATE_GAME_OVER:
                self.player1.draw(self.screen)
                self.player2.draw(self.screen)

                game_over_text = self.game_over_font.render(f"GAME OVER! {self.winner} Wins!", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                self.screen.blit(game_over_text, game_over_rect)

                restart_text = self.font.render("Press 'R' to Restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                self.screen.blit(restart_text, restart_rect)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()