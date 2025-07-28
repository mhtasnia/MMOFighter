import pygame
import sys
from settings import *
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.ATTACK_SOUND = pygame.mixer.Sound('MMOFighter/assets/sounds/attack.mp3')
        self.BLOCK_SOUND = pygame.mixer.Sound('MMOFighter/assets/sounds/block.mp3')
        self.JUMP_SOUND = pygame.mixer.Sound('MMOFighter/assets/sounds/jump.mp3')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.player = Player(100, 100, "MMOFighter/assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("MMOFighter/assets/characters/battleground.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.player1 = Player(100, 200, "MMOFighter/assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.player2 = Player(700, 200, "MMOFighter/assets/characters/character2.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)

        self.font = pygame.font.SysFont("Arial", 30)
        self.controls_font = pygame.font.SysFont("Arial", CONTROLS_FONT_SIZE)
        self.title_font = pygame.font.SysFont("Arial", TITLE_FONT_SIZE, bold=True)
        self.game_over_font = pygame.font.SysFont("Arial", GAME_OVER_FONT_SIZE, bold=True)
        self.game_state = GAME_STATE_MENU
        self.paused = False

        pygame.mixer.music.load("MMOFighter/assets/sounds/background-music-happy-375038.mp3")
        pygame.mixer.music.play(-1)


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
        border_color = (30, 30, 30)
        border_thickness = 3

        inner_rect = pygame.Rect(button_rect.x + border_thickness,
                                 button_rect.y + border_thickness,
                                 button_rect.width - 2 * border_thickness,
                                 button_rect.height - 2 * border_thickness)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, border_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, active_color, inner_rect, border_radius=7)
            if click[0] == 1 and action is not None:
                pygame.time.delay(200)
                action()
        else:
            pygame.draw.rect(self.screen, border_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, inactive_color, inner_rect, border_radius=7)

        self.draw_text(text, x, y, text_color, font=self.font)
        return button_rect

    def draw_health_bar(self, player, x, y):
        ratio = player.health / PLAYER_HEALTH
        pygame.draw.rect(self.screen, RED, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.screen, GREEN, (x, y, HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))

    def draw_player_names_and_health(self):
        self.draw_text("Player 1", 20 + HEALTH_BAR_WIDTH // 2, 10, DARK_GREEN)
        self.draw_health_bar(self.player1, 20, 20)

        self.draw_text("VS", WIDTH // 2, 30, WHITE)

        self.draw_text("Player 2", WIDTH - HEALTH_BAR_WIDTH // 2 - 20, 10, DARK_GREEN)
        self.draw_health_bar(self.player2, WIDTH - HEALTH_BAR_WIDTH - 20, 20)

    def draw_power_meter(self, player, x, y):
        ratio = player.power_meter / POWER_METER_MAX
        pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.screen, BLUE, (x, y, HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))

    def reset_game(self):
        self.player1 = Player(100, 200, "MMOFighter/assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.player2 = Player(700, 200, "MMOFighter/assets/characters/character2.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.game_state = GAME_STATE_RUNNING
        self.paused = False

    def set_game_state(self, state):
        self.game_state = state

    def back_to_main_menu(self):
        self.game_state = GAME_STATE_MENU
        self.paused = False # Ensure paused flag is reset
        self.player1 = Player(100, 200, "assets/characters/character1.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)
        self.player2 = Player(700, 200, "assets/characters/character2.png", self.ATTACK_SOUND, self.BLOCK_SOUND, self.JUMP_SOUND)


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
                    # Added 'T' key for starting a new game from anywhere for convenience
                    if event.key == pygame.K_t:
                        if self.game_state in [GAME_STATE_MENU, GAME_STATE_PAUSED, GAME_STATE_GAME_OVER]:
                            self.reset_game()

                if self.game_state == GAME_STATE_MENU:
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

            self.screen.blit(self.background, (0, 0))

            if self.game_state == GAME_STATE_MENU:
                self.draw_text("MMO FIGHTER", WIDTH // 2, HEIGHT // 5, WHITE, font=self.title_font)

                self.draw_button("New Game", WIDTH // 2, HEIGHT // 2 - 80, 200, 60, BUTTON_COLOR, DARK_GREEN, WHITE, self.reset_game)
                self.draw_button("Quit", WIDTH // 2, HEIGHT // 2, 200, 60, BUTTON_COLOR, RED, WHITE, self.quit_game)

                # New instructions added here
                self.draw_text("Press 'P' to Pause/Resume (during game)", WIDTH // 2, HEIGHT // 2 + 80, WHITE, font=self.controls_font)
                self.draw_text("Press 'T' to Start New Game", WIDTH // 2, HEIGHT // 2 + 110, WHITE, font=self.controls_font)

                controls_panel_width = WIDTH * 0.9
                controls_panel_height = HEIGHT * 0.35
                controls_panel_x = (WIDTH - controls_panel_width) // 2
                controls_panel_y = HEIGHT - controls_panel_height - 10
                controls_panel_rect = pygame.Rect(controls_panel_x, controls_panel_y, controls_panel_width, controls_panel_height)
                # Changed background of the controls box to grey (128, 128, 128) with alpha
                pygame.draw.rect(self.screen, (128, 128, 128, 150), controls_panel_rect, border_radius=15)

                player1_controls_x = controls_panel_x + controls_panel_width // 4
                # Changed text color to DARK_GREEN
                self.draw_text("Player 1 Controls:", player1_controls_x, controls_panel_y + 25, DARK_GREEN, font=self.controls_font)
                self.draw_text("Move: A/D", player1_controls_x, controls_panel_y + 55, DARK_GREEN, font=self.controls_font)
                self.draw_text("Jump: W", player1_controls_x, controls_panel_y + 80, DARK_GREEN, font=self.controls_font)
                self.draw_text("Light Attack: F", player1_controls_x, controls_panel_y + 105, DARK_GREEN, font=self.controls_font)
                self.draw_text("Heavy Attack: G", player1_controls_x, controls_panel_y + 130, DARK_GREEN, font=self.controls_font)
                self.draw_text("Special Move: H", player1_controls_x, controls_panel_y + 155, DARK_GREEN, font=self.controls_font)
                self.draw_text("Block: S", player1_controls_x, controls_panel_y + 180, DARK_GREEN, font=self.controls_font)

                player2_controls_x = controls_panel_x + controls_panel_width * 3 // 4
                # Changed text color to DARK_GREEN
                self.draw_text("Player 2 Controls:", player2_controls_x, controls_panel_y + 25, DARK_GREEN, font=self.controls_font)
                self.draw_text("Move: Left/Right Arrow", player2_controls_x, controls_panel_y + 55, DARK_GREEN, font=self.controls_font)
                self.draw_text("Jump: Up Arrow", player2_controls_x, controls_panel_y + 80, DARK_GREEN, font=self.controls_font)
                self.draw_text("Light Attack: RCtrl", player2_controls_x, controls_panel_y + 105, DARK_GREEN, font=self.controls_font)
                self.draw_text("Heavy Attack: RShift", player2_controls_x, controls_panel_y + 130, DARK_GREEN, font=self.controls_font)
                self.draw_text("Special Move: / (Slash)", player2_controls_x, controls_panel_y + 155, DARK_GREEN, font=self.controls_font)
                self.draw_text("Block: Down Arrow", player2_controls_x, controls_panel_y + 180, DARK_GREEN, font=self.controls_font)

            elif self.game_state == GAME_STATE_RUNNING:
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

                self.player1.update(self.player2)
                self.player2.update(self.player1)

                if self.player1.health <= 0:
                    self.game_state = GAME_STATE_GAME_OVER
                    self.winner = "Player 2"
                elif self.player2.health <= 0:
                    self.game_state = GAME_STATE_GAME_OVER
                    self.winner = "Player 1"

                self.player1.draw(self.screen)
                self.player2.draw(self.screen)

                self.draw_player_names_and_health()

                self.draw_power_meter(self.player1, 20, 50)
                self.draw_power_meter(self.player2, WIDTH - HEALTH_BAR_WIDTH - 20, 50)

                if self.player1.combo_count > 0:
                    self.draw_text(f"P1 Combo: {self.player1.combo_count}", 100, 80, WHITE)
                if self.player2.combo_count > 0:
                    self.draw_text(f"P2 Combo: {self.player2.combo_count}", WIDTH - 100, 80, WHITE)

            elif self.game_state == GAME_STATE_PAUSED:
                # Draw a semi-transparent overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128)) # Black with 128 alpha (half transparent)
                self.screen.blit(overlay, (0, 0))
                self.draw_text("PAUSED", WIDTH // 2, HEIGHT // 2 - 100, WHITE, font=self.game_over_font)

                # Resume Button
                self.draw_button("Resume", WIDTH // 2, HEIGHT // 2, 200, 60, BUTTON_COLOR, DARK_GREEN, WHITE, lambda: self.set_game_state(GAME_STATE_RUNNING))

                # Back to Main Menu Button
                self.draw_button("Main Menu", WIDTH // 2, HEIGHT // 2 + 80, 200, 60, BUTTON_COLOR, RED, WHITE, self.back_to_main_menu)


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