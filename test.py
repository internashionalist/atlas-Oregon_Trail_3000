import pygame
import os

os.environ["DISPLAY"] = "host.docker.internal:0"
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Test")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 255, 0))
    pygame.display.flip()

pygame.quit()