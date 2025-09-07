import pygame
pygame.init()

screen = pygame.display.set_mode((500, 500))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 0), (250, 100), 50)
    pygame.draw.circle(screen, (0, 180, 0), (250, 250), 50)
    pygame.draw.circle(screen, (255, 0, 0), (250, 400), 50)

    pygame.display.flip()

pygame.quit()
