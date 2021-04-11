from constants import *

class Enemy:
    def __init__(self):
        x_pos = random.randint(0, SCREEN_WIDTH-ENEMY_IMG_WIDTH)
        y_pos = random.randint(0, int(.2 * SCREEN_HEIGHT))
        self.pos = point.Point(x_pos, y_pos)
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

    def draw(self, screen):
        screen.blit(ENEMY_IMG, self.get_pos().get_tuple())

    def death_sound(self, mixer):
        death_sound = mixer.Sound(ENEMY_DEATH_SOUND_LOC)
        death_sound.play()
