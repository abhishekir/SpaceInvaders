import pygame
import random

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 50)

GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"

PLAYER_IMAGE_LOC = "media/player.png"
PLAYER_IMG = pygame.image.load(PLAYER_IMAGE_LOC)
PLAYER_IMG_WIDTH = PLAYER_IMG.get_width()
PLAYER_IMG_HEIGHT = PLAYER_IMG.get_height()
PLAYER_X_INIT = (SCREEN_WIDTH / 2) - (PLAYER_IMG_WIDTH / 2)  # half on screen x-axis
PLAYER_Y_INIT = (SCREEN_HEIGHT * .75) + (PLAYER_IMG_HEIGHT / 2)  # 3/4 down on screen y-axis
PLAYER_VELOCITY = .5 # pixels per tick

ENEMY_IMG_LOC = "media/alien.png"
ENEMY_IMG = pygame.image.load(ENEMY_IMG_LOC)
ENEMY_IMG_WIDTH = ENEMY_IMG.get_width()
ENEMY_IMG_HEIGHT = ENEMY_IMG.get_height()
ENEMY_VELOCITY = .05 # pixels per tick

def initialize():
    # Initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)
    icon = pygame.image.load(GAME_ICON)
    pygame.display.set_icon(icon)

    return screen

class Enemy:
    def __init__(self):
        self.x_pos = random.randint(0, SCREEN_WIDTH-ENEMY_IMG_WIDTH)
        self.y_pos = random.randint(0, int(.2 * SCREEN_HEIGHT))

    def move_enemy(self):
        new_y = self.y_pos + ENEMY_VELOCITY
        if (new_y <= SCREEN_HEIGHT - ENEMY_IMG_HEIGHT):
            self.y_pos = new_y

    def get_pos(self):
        return (self.x_pos, self.y_pos)

    def draw(enemy):
        screen.blit(ENEMY_IMG, enemy.get_pos())



class Player:
    def __init__(self):
        self.x_pos = PLAYER_X_INIT
        self.y_pos = PLAYER_Y_INIT
        self.move_direction = [False, False, False, False] # Left, Right, Up, Down

    def toggle_left(self):
        self.move_direction[0] = not self.move_direction[0]

    def toggle_right(self):
        self.move_direction[1] = not self.move_direction[1]

    def toggle_up(self):
        self.move_direction[2] = not self.move_direction[2]

    def toggle_down(self):
        self.move_direction[3] = not self.move_direction[3]

    def move_player(self):
        if (self.move_direction[0]): # Move LEFT
            new_x = self.x_pos - PLAYER_VELOCITY
            if (new_x >= 0): # Left bound check
                self.x_pos = new_x

        if (self.move_direction[1]): # Move RIGHT
            new_x = self.x_pos + PLAYER_VELOCITY
            if (new_x <= SCREEN_WIDTH - PLAYER_IMG_WIDTH): # Right bound check
                self.x_pos = new_x

        if (self.move_direction[2]): # Move UP
            new_y = self.y_pos - PLAYER_VELOCITY
            if (new_y >= SCREEN_HEIGHT * .75): # Up bound check (limit 3/4 up the screen)
                self.y_pos = new_y

        if (self.move_direction[3]): # Move DOWN
            new_y = self.y_pos + PLAYER_VELOCITY
            if (new_y <= SCREEN_HEIGHT - PLAYER_IMG_HEIGHT): # Down bound check
                self.y_pos = new_y

    # def change_pos(self, x_change, y_change):
    #     self.x_pos += x_change
    #     self.y_pos += y_change

    def get_pos(self):
        return (self.x_pos, self.y_pos)

    def draw(player):
        screen.blit(PLAYER_IMG, player.get_pos())


def main(screen):
    # Game Loop
    running = True
    player = Player()
    enemy = Enemy()

    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    print("left key down")
                    player.toggle_left()
                if event.key == pygame.K_RIGHT:
                    print("right key down")
                    player.toggle_right()
                if event.key == pygame.K_UP:
                    print("up key down")
                    player.toggle_up()
                if event.key == pygame.K_DOWN:
                    print("down key down")
                    player.toggle_down()
            if event.type == pygame.KEYUP:
                print("key up")
                if event.key == pygame.K_LEFT:
                    player.toggle_left()
                if event.key == pygame.K_RIGHT:
                    player.toggle_right()
                if event.key == pygame.K_UP:
                    player.toggle_up()
                if event.key == pygame.K_DOWN:
                    player.toggle_down()

        if running:
            player.move_player()
            player.draw()

            enemy.move_enemy()
            enemy.draw()

            pygame.display.update()
        else:
            pygame.quit()


if __name__ == "__main__":
    screen = initialize()
    main(screen)
