from constants import *

class Bullet:
    def __init__(self, point):
        self.pos = point
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

    def draw(self, screen):
        screen.blit(BULLET_IMG, self.get_pos().get_tuple())
