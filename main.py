import pygame
import random

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 50)
BACKGROUND_IMG_LOC = "media/background.png"
BACKGROUND_IMG = pygame.image.load(BACKGROUND_IMG_LOC)

GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"

PLAYER_IMAGE_LOC = "media/player.png"
PLAYER_IMG = pygame.image.load(PLAYER_IMAGE_LOC)
PLAYER_IMG_WIDTH = PLAYER_IMG.get_width()
PLAYER_IMG_HEIGHT = PLAYER_IMG.get_height()
PLAYER_X_INIT = (SCREEN_WIDTH / 2) - (PLAYER_IMG_WIDTH / 2)  # half on screen x-axis
PLAYER_Y_INIT = (SCREEN_HEIGHT * .8) + (PLAYER_IMG_HEIGHT / 2)  # 3/4 down on screen y-axis
PLAYER_VELOCITY = 4 # pixels per tick

ENEMY_IMG_LOC = "media/alien.png"
ENEMY_IMG = pygame.image.load(ENEMY_IMG_LOC)
ENEMY_IMG_WIDTH = ENEMY_IMG.get_width()
ENEMY_IMG_HEIGHT = ENEMY_IMG.get_height()
ENEMY_X_VELOCITY = 1.25 # pixels per tick
ENEMY_Y_VELOCITY = .2 # pixels per tick

BULLET_IMG_LOC = "media/bullet.png"
BULLET_IMG = pygame.image.load(BULLET_IMG_LOC)
BULLET_IMG_WIDTH = BULLET_IMG.get_width()
BULLET_IMG_HEIGHT = BULLET_IMG.get_height()
BULLET_VELOCITY = 6


def initialize():
    # Initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)
    icon = pygame.image.load(GAME_ICON)
    pygame.display.set_icon(icon)

    return screen


class Point:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def set_x(self, x):
        self.x_pos = x

    def set_y(self, y):
        self.y_pos = y

    def get_tuple(self):
        return (self.x_pos, self.y_pos)


class Enemy:
    def __init__(self):
        x_pos = random.randint(0, SCREEN_WIDTH-ENEMY_IMG_WIDTH)
        y_pos = random.randint(0, int(.2 * SCREEN_HEIGHT))
        self.pos = Point(x_pos, y_pos)
        self.moving_right = random.choice([True, False])

    def get_pos(self):
        return self.pos

    def toggle_moving_direction(self):
        self.moving_right = not self.moving_right

    def move_enemy(self):
        if (self.moving_right):
            new_x = self.get_pos().get_x() + ENEMY_X_VELOCITY
            if (new_x <= SCREEN_WIDTH - ENEMY_IMG_WIDTH):  # Right bound check
                self.get_pos().set_x(new_x)
            else:
                self.toggle_moving_direction()
        else:
            new_x = self.get_pos().get_x() - ENEMY_X_VELOCITY
            if (new_x >= 0): # Left bound check
                self.get_pos().set_x(new_x)
            else:
                self.toggle_moving_direction()

        new_y = self.get_pos().get_y() + ENEMY_Y_VELOCITY
        if (new_y <= SCREEN_HEIGHT - ENEMY_IMG_HEIGHT):
            self.get_pos().set_y(new_y)

    def draw(self):
        screen.blit(ENEMY_IMG, self.get_pos().get_tuple())


class Bullet:
    def __init__(self, point):
        adjusted_x_pos = point.get_x() + (PLAYER_IMG_WIDTH / 2) - (BULLET_IMG_WIDTH / 2)
        self.pos = Point(adjusted_x_pos, point.get_y())
        self.off_screen = False

    def get_pos(self):
        return self.pos

    def get_off_screen(self):
        return self.off_screen

    def move_bullet(self):
        new_y = self.get_pos().get_y() - BULLET_VELOCITY
        # if (new_y >= -BULLET_IMG_HEIGHT*2): # Bullet out of bounds check
        if (new_y >= 0):
            self.get_pos().set_y(new_y)
        else:
            self.off_screen = True

    def draw(self):
        screen.blit(BULLET_IMG, self.get_pos().get_tuple())


class Player:
    def __init__(self):
        x_pos = PLAYER_X_INIT
        y_pos = PLAYER_Y_INIT
        self.pos = Point(x_pos, y_pos)
        self.move_direction = [False, False, False, False] # Left, Right, Up, Down

    def get_pos(self):
        return self.pos

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
            new_x = self.get_pos().get_x() - PLAYER_VELOCITY
            if (new_x >= 0): # Left bound check
                self.get_pos().set_x(new_x)

        if (self.move_direction[1]): # Move RIGHT
            new_x = self.get_pos().get_x() + PLAYER_VELOCITY
            if (new_x <= SCREEN_WIDTH - PLAYER_IMG_WIDTH): # Right bound check
                self.get_pos().set_x(new_x)

        if (self.move_direction[2]): # Move UP
            new_y = self.get_pos().get_y() - PLAYER_VELOCITY
            if (new_y >= SCREEN_HEIGHT * .75): # Up bound check (limit 3/4 up the screen)
                self.get_pos().set_y(new_y)

        if (self.move_direction[3]): # Move DOWN
            new_y = self.get_pos().get_y() + PLAYER_VELOCITY
            if (new_y <= SCREEN_HEIGHT - PLAYER_IMG_HEIGHT): # Down bound check
                self.get_pos().set_y(new_y)

    def draw(self):
        screen.blit(PLAYER_IMG, self.get_pos().get_tuple())


def main(screen):
    # Game Loop
    running = True
    player = Player()
    enemyList = [Enemy()]
    bulletList = []

    while running:
        # screen.fill(BACKGROUND_COLOR)
        screen.blit(BACKGROUND_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    # print("left key down")
                    player.toggle_left()
                if event.key == pygame.K_RIGHT:
                    # print("right key down")
                    player.toggle_right()
                if event.key == pygame.K_UP:
                    # print("up key down")
                    player.toggle_up()
                if event.key == pygame.K_DOWN:
                    # print("down key down")
                    player.toggle_down()
                if event.key == pygame.K_SPACE:
                    # print("space bar down")
                    bulletList.append(Bullet(player.get_pos()))
            if event.type == pygame.KEYUP:
                # print("key up")
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

            for bullet in bulletList:
                if bullet.get_off_screen():
                    bulletList.remove(bullet)
                else:
                    bullet.move_bullet()
                    bullet.draw()

            for enemy in enemyList:
                enemy.move_enemy()
                enemy.draw()

            pygame.display.update()
        else:
            pygame.quit()


if __name__ == "__main__":
    screen = initialize()
    main(screen)
