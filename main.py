import pygame


# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 50)

GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"

PLAYER_IMAGE_LOC = "media/player.png"
PLAYER_IMG = pygame.image.load(PLAYER_IMAGE_LOC)
PLAYER_X_INIT = (SCREEN_WIDTH / 2) - (PLAYER_IMG.get_width() / 2)  # half on screen x-axis
PLAYER_Y_INIT = (SCREEN_HEIGHT * .75) + (PLAYER_IMG.get_height() / 2)  # 3/4 down on screen y-axis
PLAYER_VELOCITY = .5 # pixels per tick


def initialize():
    # Initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)
    icon = pygame.image.load(GAME_ICON)
    pygame.display.set_icon(icon)

    return screen


class Player:
    def __init__(self):
        self.x_pos = PLAYER_X_INIT
        self.y_pos = PLAYER_Y_INIT
        self.move_direction = [False, False, False, False] # Left, Right, Up, Down

    def toggle_left(self):
        self.move_direction[0] = not self.move_direction[0]

    def toggle_right(self):
        self.move_direction[1] = not self.move_direction[1]

    def move_player(self):
        if (self.move_direction[0]):
            self.x_pos -= (PLAYER_VELOCITY)
        if (self.move_direction[1]):
            self.x_pos += PLAYER_VELOCITY
        if (self.move_direction[2]):
            self.y_pos -= PLAYER_VELOCITY
        if (self.move_direction[3]):
            self.y_pos += PLAYER_VELOCITY

    # def change_pos(self, x_change, y_change):
    #     self.x_pos += x_change
    #     self.y_pos += y_change

    def get_pos(self):
        return (self.x_pos, self.y_pos)

    def draw_player(player):
        screen.blit(PLAYER_IMG, player.get_pos())


def main(screen):
    # Game Loop
    running = True
    player = Player()

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
            if event.type == pygame.KEYUP:
                print("key up")
                if event.key == pygame.K_LEFT:
                    player.toggle_left()
                if event.key == pygame.K_RIGHT:
                    player.toggle_right()

        if running:
            player.move_player()
            player.draw_player()
            pygame.display.update()
        else:
            pygame.quit()


if __name__ == "__main__":
    screen = initialize()
    main(screen)
