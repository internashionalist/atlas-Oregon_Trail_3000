import pygame
import pygame_menu
from pygame_menu import themes

surface = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE | pygame.FULLSCREEN)

def start_the_game():
    pass

def bad_ending():
    pass

def good_ending():
    pass

def mainmenu():
    mainmenu = pygame_menu.Menu('Oregon Trail', 1200, 900,
                                theme=themes.THEME_ORANGE)
    mainmenu.add.label('Welcome to Mars!')
    mainmenu.add.text_input('Name: ', default='username', maxchar=25)
    mainmenu.add.button('Play', start_the_game)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
        pygame.display.update()

if __name__ == '__main__':
    if not pygame.get_init():
        pygame.init()

    mainmenu()
