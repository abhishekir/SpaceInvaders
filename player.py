from constants import *

class Player:
    def __init__(self):
        x_pos = PLAYER_X_INIT
        y_pos = PLAYER_Y_INIT
        self.pos = point.Point(x_pos, y_pos)
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
        bullet_pos = point.Point(adjusted_x_pos, self.get_pos().get_y())
        new_bullet = bullet.Bullet(bullet_pos)
        self.bullet_list.append(new_bullet)
        self.last_shot_time = pygame.time.get_ticks()

    # Manages the player's bullet list
    # - Existing Bullets
    #   - checks out of bounds bullets and removes them from bullet list
    #   - checks if collided and removes them from bullet list
    #   - moves existing bullets
    # - New Bullets
    #   - creates new bullets if firing and if possible
    def handle_bullets(self):
        # existing bullet handling
        for bullet in self.get_bullet_list():
            if bullet.get_off_screen() or bullet.get_collision():
                self.get_bullet_list().remove(bullet)
            else:
                self.move_player_bullet(bullet)
        # new bullet handling
        if (self.get_firing()):
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_shot_time > PLAYER_BULLET_INTERVAL):
                self.add_bullet()

    def move_player_bullet(self, bullet):
        new_y = bullet.get_pos().get_y() - BULLET_VELOCITY
        bullet.move_bullet(point.Point(bullet.get_pos().get_x(), new_y))

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

    def draw(self, screen):
        screen.blit(PLAYER_IMG, self.get_pos().get_tuple())
