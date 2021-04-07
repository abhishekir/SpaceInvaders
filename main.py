import pygame

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (192, 192, 192)
GAME_CAPTION = "Space Invaders"
GAME_ICON = "media/game_icon.png"
PLAYER_IMAGE = "media/player.png"

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
def player():
    playerImg = pygame.image.load(PLAYER_IMAGE)
    playerX = (SCREEN_WIDTH / 2) - (playerImg.get_width() / 2) # half on screen x-axis
    playerY = (SCREEN_HEIGHT * .75) + (playerImg.get_height() / 2) # 3/4 down on screen y-axis
    # print(playerX, playerY)
    screen.blit(playerImg, (playerX, playerY))

def main(screen):
    # Game Loop
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    # pygame.quit()

        player()

        pygame.display.update()

if __name__ == "__main__":
    screen = initialize()
    main(screen)
