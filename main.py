import pygame


# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (192, 192, 192)
GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"
PLAYER_IMAGE_LOC = "media/player.png"
PLAYER_IMG = pygame.image.load(PLAYER_IMAGE_LOC)
PLAYER_X_INIT = (SCREEN_WIDTH / 2) - (PLAYER_IMG.get_width() / 2)  # half on screen x-axis
PLAYER_Y_INIT = (SCREEN_HEIGHT * .75) + (PLAYER_IMG.get_height() / 2)  # 3/4 down on screen y-axis

def initialize():
    # Initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)
    icon = pygame.image.load(GAME_ICON)
    pygame.display.set_icon(icon)

    return screen


# Player
def player(playerX, playerY):
    # print(playerX, playerY)
    screen.blit(PLAYER_IMG, (playerX, playerY))


def main(screen):
    # Game Loop
    running = True
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
                if event.key == pygame.K_RIGHT:
                    print("right key down")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    print("key up")

        if not running:
            pygame.quit()
        else:
            player(PLAYER_X_INIT, PLAYER_Y_INIT)
            pygame.display.update()


if __name__ == "__main__":
    screen = initialize()
    main(screen)
