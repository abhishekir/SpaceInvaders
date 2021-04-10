import pygame
import random
import math

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
PLAYER_BULLET_INTERVAL = 300 # milliseconds between firing a bullet

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

    def point_dist(self, other):
        other_x = other.get_x()
        other_y = other.get_y()
        return math.sqrt((other_x - self.get_x()) ** 2 + (other_y - self.get_y()) ** 2)


class Enemy:
    def __init__(self):
        x_pos = random.randint(0, SCREEN_WIDTH-ENEMY_IMG_WIDTH)
        y_pos = random.randint(0, int(.2 * SCREEN_HEIGHT))
        self.pos = Point(x_pos, y_pos)
        self.moving_right = random.choice([True, False])
        self.collision = False

    def get_pos(self):
        return self.pos

    def toggle_moving_direction(self):
        self.moving_right = not self.moving_right

    def get_collision(self):
        return self.collision

    def set_collided(self):
        self.collision = True

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
        self.pos = Point(point.get_x(), point.get_y())
        self.off_screen = False
        self.collision = False

    def get_pos(self):
        return self.pos

    def get_off_screen(self):
        return self.off_screen

    def get_collision(self):
        return self.collision

    def set_collided(self):
        self.collision = True

    # set the boolean determining if a bullet is within the game screen
    def set_off_screen(self):
        if (0 <= self.get_pos().get_x() <= SCREEN_WIDTH-BULLET_IMG_WIDTH
                and 0 <= self.get_pos().get_y() <= SCREEN_HEIGHT-BULLET_IMG_HEIGHT):
            self.off_screen = False
        else:
            self.off_screen = True

    def move_bullet(self, point):
        self.get_pos().set_x(point.get_x())
        self.get_pos().set_y(point.get_y())
        self.set_off_screen()

    def draw(self):
        screen.blit(BULLET_IMG, self.get_pos().get_tuple())


class Player:
    def __init__(self):
        x_pos = PLAYER_X_INIT
        y_pos = PLAYER_Y_INIT
        self.pos = Point(x_pos, y_pos)
        self.move_direction = [False, False, False, False] # Left, Right, Up, Down
        self.bullet_list = []
        self.firing = False
        self.last_shot_time = 0

    def get_pos(self):
        return self.pos

    def get_bullet_list(self):
        return self.bullet_list

    def get_firing(self):
        return self.firing

    def add_bullet(self):
        adjusted_x_pos = self.get_pos().get_x() + (PLAYER_IMG_WIDTH / 2) - (BULLET_IMG_WIDTH / 2)
        bullet_pos = Point(adjusted_x_pos, self.get_pos().get_y())
        bullet = Bullet(bullet_pos)
        self.bullet_list.append(bullet)
        self.last_shot_time = pygame.time.get_ticks()

    # Manages the player's bullet list
    # - Existing Bullets
    #   - checks out of bounds bullets and removes them from bullet list
    #   - checks if collided and removes them from bullet list
    #   - moves existing bullets
    #   - draws existing bullets
    # - New Bullets
    #   - creates new bullets if firing and if possible
    def handle_bullets(self):
        # existing bullet handling
        for bullet in self.get_bullet_list():
            if bullet.get_off_screen() or bullet.get_collision():
                self.get_bullet_list().remove(bullet)
            else:
                self.move_player_bullet(bullet)
                bullet.draw()
        # new bullet handling
        if (self.get_firing()):
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_shot_time > PLAYER_BULLET_INTERVAL):
                self.add_bullet()

    def move_player_bullet(self, bullet):
        new_y = bullet.get_pos().get_y() - BULLET_VELOCITY
        bullet.move_bullet(Point(bullet.get_pos().get_x(), new_y))

    def toggle_firing(self):
        self.firing = not self.get_firing()

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


# manages the repeating logic of the game
# - collision checking, enemy spawning, removing
class Game_Handler:
    def __init__(self):
        self.player = Player()
        self.enemyList = [Enemy()]
        self.last_enemy_spawn_time = 0
        self.enemy_spawn_rate = 100 # milliseconds between new enemy spawn

    def get_player(self):
        return self.player

    def get_enemyList(self):
        return self.enemyList

    def main_handler(self):
        self.get_player().move_player()
        self.get_player().draw()
        # handles managing and drawing player bullets
        self.get_player().handle_bullets()

        # handles removing collided enemies
        # handles moving, drawing existing enemies
        self.enemy_handler()

        # handles setting collided flag for enemies with bullets
        self.collision_handler()

    def check_collision(self, object1, object1_width, object1_height,
                        object2, object2_width, object2_height):
        if (object1.get_pos().point_dist(object2.get_pos()) < (object1_height + object2_height)): # initial collision check
            # print("passed near collision check")
            if ((object1.get_pos().get_x() < object2.get_pos().get_x() + object2_width
                and object1.get_pos().get_x() + object1_width > object2.get_pos().get_x())
                and
                (object1.get_pos().get_y() < object2.get_pos().get_y() + object2_height
                and object1.get_pos().get_y() + object1_height > object2.get_pos().get_y())):
                # print("passed actual collision check")
                # print("Object1 x: %d, y: %d\nObject2 x: %d, y: %d"
                #       % (object1.get_pos().get_x(), object1.get_pos().get_y(),
                #       object2.get_pos().get_x(), object2.get_pos().get_y()))

                object1.set_collided()
                object2.set_collided()
                return True
            else:
                # print("failed close check")
                return False
        else:
            # print("failed initial check")
            return False

    def enemy_handler(self):
        for enemy in self.get_enemyList():
            if enemy.get_collision():
                self.get_enemyList().remove(enemy)
            else:
                enemy.move_enemy()
                enemy.draw()

    def collision_handler(self):
        for bullet in self.get_player().get_bullet_list():
            for enemy in self.get_enemyList():
                self.check_collision(bullet, BULLET_IMG_WIDTH, BULLET_IMG_HEIGHT,
                                     enemy, ENEMY_IMG_WIDTH, ENEMY_IMG_HEIGHT)


def main(screen):
    # Game Loop
    running = True
    handler = Game_Handler()

    while running:
        # screen.fill(BACKGROUND_COLOR)
        screen.blit(BACKGROUND_IMG, (0, 0))

        # Key Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    handler.get_player().toggle_left()
                if event.key == pygame.K_RIGHT:
                    handler.get_player().toggle_right()
                if event.key == pygame.K_UP:
                    handler.get_player().toggle_up()
                if event.key == pygame.K_DOWN:
                    handler.get_player().toggle_down()
                if event.key == pygame.K_SPACE:
                    handler.get_player().toggle_firing()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    handler.get_player().toggle_left()
                if event.key == pygame.K_RIGHT:
                    handler.get_player().toggle_right()
                if event.key == pygame.K_UP:
                    handler.get_player().toggle_up()
                if event.key == pygame.K_DOWN:
                    handler.get_player().toggle_down()
                if event.key == pygame.K_SPACE:
                    handler.get_player().toggle_firing()

        # Game Loop Logic Handler
        if running:
            handler.main_handler()
            pygame.display.update()
        else:
            pygame.quit()


if __name__ == "__main__":
    screen = initialize()
    main(screen)
