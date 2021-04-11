from constants import *

def initialize():
    # Initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)
    icon = pygame.image.load(GAME_ICON)
    pygame.display.set_icon(icon)

    # Load, play background music
    mixer.music.load(BACKGROUND_MUSIC_LOC)
    mixer.music.play(-1)

    return screen, mixer


# manages the repeating logic of the game
# - collision checking, enemy spawning, removing
class Game_Handler:
    def __init__(self):
        self.player = player.Player()
        self.enemyList = [enemy.Enemy()]
        self.last_enemy_spawn_time = 0
        self.max_enemy_count = 8
        self.enemy_spawn_rate = 3000 # milliseconds between new enemy spawn
        self.game_score = 0

    def get_player(self):
        return self.player

    def get_enemyList(self):
        return self.enemyList

    def get_score(self):
        return self.game_score

    def main_handler(self, mixer):
        self.get_player().move_player()
        # handles managing and drawing player bullets
        self.get_player().handle_bullets(mixer)

        # handles removing collided enemies
        # handles moving, existing enemies
        self.enemy_handler(mixer)

        # handles setting collided flag for enemies with bullets
        self.collision_handler()

    def collision_handler(self):
        for bullet in self.get_player().get_bullet_list():
            for enemy in self.get_enemyList():
                self.check_collision(bullet, BULLET_IMG_WIDTH, BULLET_IMG_HEIGHT,
                                     enemy, ENEMY_IMG_WIDTH, ENEMY_IMG_HEIGHT)

    def check_collision(self, object1, object1_width, object1_height,
                        object2, object2_width, object2_height):
        # rough initial collision check based on size of the objects
        if (object1.get_pos().point_dist(object2.get_pos()) < (object1_height + object2_height)):
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

    def enemy_handler(self, mixer):
        for enemy in self.get_enemyList():
            if enemy.get_collision():
                self.game_score += 1
                enemy.death_sound(mixer)
                self.get_enemyList().remove(enemy)
            else:
                enemy.move_enemy()
        self.add_enemy()

    def add_enemy(self):
        if (len(self.get_enemyList()) < self.max_enemy_count):
            curr_time = pygame.time.get_ticks()
            if (curr_time - self.last_enemy_spawn_time > self.enemy_spawn_rate):
                new_enemy = enemy.Enemy()
                self.get_enemyList().append(new_enemy)
                self.last_enemy_spawn_time = curr_time

    def draw_score(self, screen):
        font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
        score_text_render = font.render("Score: " + str(self.get_score()), True, SCORE_FONT_COLOR)
        screen.blit(score_text_render, SCORE_TEXT_POS)


def main(screen, mixer):
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

        # Game in-progress
        if running:
            # Game-loop Logic Handler
            handler.main_handler(mixer)

            # Draw everything here
            handler.get_player().draw(screen)
            for bullet in handler.get_player().get_bullet_list():
                bullet.draw(screen)
            for enemy in handler.get_enemyList():
                enemy.draw(screen)

            handler.draw_score(screen)

            pygame.display.update()
        else:
            pygame.quit()


if __name__ == "__main__":
    init = initialize()
    screen = init[0]
    mixer = init[1]
    main(screen, mixer)
