import pygame
import pygame_menu
from pygame_menu import themes
import sys
import os

os.environ["DISPLAY"] = "host.docker.internal:0"
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init() # start 'er up

screen_width, screen_height = 1920, 1080
surface = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.FULLSCREEN)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

encounters = [
    {
      "text": "something something DOOM",
      "choices": [
        {"text": "Fight (-20 health)", "health_change": -20},
        {"text": "Flee (-15 health)", "health_change": -15},
        {"text": "Romance (-5 health)", "health_change": -5}
      ]
    },
    # more encounters
]

def display_text(screen, text, x, y):
    rendered_text = font.render(text, True, GREEN)
    screen.blit(rendered_text, (x, y))

def health_bar(screen, health):
    pygame.draw.rect(screen, RED, (10, 50, 200, 50))
    pygame.draw.rect(screen, GREEN, (10, 50, health * 2, 50))

def encounter_choice(encounter):
    surface.fill(BLACK)
    display_text(surface, encounter["text"], 100, 300)

    for i, choice in enumerate(encounter["choices"]):
        display_text(surface, f"{i + 1}: {choice['text']}", 100, 300 + i * 50)
    
    pygame.display.flip()

    while True: # main game loop draft
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # key presses for choices
                if event.key == pygame.K_1:
                    return encounter["choices"][0]["health_change"]
                if event.key == pygame.K_2:
                    return encounter["choices"][1]["health_change"]
                if event.key == pygame.K_3:
                    return encounter["choices"][2]["health_change"]

def bad_ending(): # DYSENTERY
    surface.fill(BLACK)
    display_text(surface, "You have died of dysentery.", 100, 300)
    pygame.display.flip()
    pygame.time.delay(5000) # is five seconds enough?

def good_ending():
    surface.fill((0, 0, 0))
    display_text(surface, "You have reached Oregon!", 100, 300)
    pygame.display.flip()
    pygame.time.delay(5000)

def start_the_game():
    health = 100 # any other variables?
    encounter_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if encounter_index >= len(encounters): # if all encounters are done
            running = False
            good_ending() if health > 0 else bad_ending()
            break

        result = encounter_choice(encounters[encounter_index]) # grab result from encounter
        health += result
        encounter_index += 1

        if health <= 0: # if you die
            running = False
            bad_ending()
            break

        surface.fill(BLACK)
        health_bar(surface, health)
        display_text(surface, f"Encounter {encounter_index}/5", 50, 150)
        pygame.display.flip()


def mainmenu():
    mainmenu = pygame_menu.Menu(
        'Oregon Trail 3000',
        screen_width // 2,
        screen_height // 2,
        theme=pygame_menu.themes.THEME_ORANGE
    )
    mainmenu.add.label('Welcome to Mars!')
    mainmenu.add.text_input('Name: ', default='username', maxchar=25)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mainmenu.update(events)
        mainmenu.draw(surface)
        pygame.display.update()

if __name__ == '__main__':
    mainmenu()
    pygame.quit()
