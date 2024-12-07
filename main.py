import pygame
import pygame_menu
from pygame_menu import themes
import sys
import os

os.environ["DISPLAY"] = "host.docker.internal:0"  # comment out for running outside docker
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init() # start 'er up
username = ''

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
      ],
      "background_image": pygame.image.load("assets/1920x1080-mars-landscape.jpg"),
      "reaction_image_1": pygame.image.load("assets/original_finale.jpg"),
      "reaction_image_2": 'pygame.image.load("FILL_IN")', # uncomment and adjust if desired
      "reaction_image_3": 'pygame.image.load("FILL_IN")'
    },
    {
      "text": "A friendly TSA Agent asks you about any anti-Skynet Affiliations",
      "choices": [
        {"text": "Fight (-20 health)", "health_change": -20},
        {"text": "Flee (-15 health)", "health_change": -15},
        {"text": "Romance (-5 health)", "health_change": -5}
      ],
      "background_image": pygame.image.load("assets/T-1000_terminator.jpg"),
      "reaction_image_1": pygame.image.load("assets/original_finale.jpg"),
      "reaction_image_2": 'pygame.image.load("FILL_IN")', # uncomment and adjust if desired
      "reaction_image_3": 'pygame.image.load("FILL_IN")'
    },
    # more encounters
]

def display_text(screen, text, x, y):
    rendered_text = font.render(text, True, GREEN)
    screen.blit(rendered_text, (x, y))

def health_bar(screen, health):
    pygame.draw.rect(screen, RED, (10, 50, 200, 50))
    pygame.draw.rect(screen, GREEN, (10, 50, health * 2, 50))

def scale_image(image, screen_width, screen_height):
    # scales an image to the current screen height
    return pygame.transform.scale(image, (screen_width, screen_height))

def encounter_choice(encounter):
    surface.fill(BLACK)
    current_screen_width, current_screen_height = surface.get_size()
    resized_encounter_image = scale_image(encounter['background_image'], current_screen_width, current_screen_height)
    surface.blit(resized_encounter_image, (0, 0))
    display_text(surface, encounter["text"] + '\n', 100, 300)

    for i, choice in enumerate(encounter["choices"]):
        display_text(surface, f"{i + 1}: {choice['text']}", 100, 350 + i * 50)

    pygame.display.flip()

    while True: # main game loop draft
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # key presses for choices
                current_screen_width, current_screen_height = surface.get_size()
                width_centered = current_screen_width / 2 - 1980 / 4
                height_centered = current_screen_height / 2 - 1080 / 4
                if event.key == pygame.K_1:
                    if isinstance(encounter['reaction_image_1'], pygame.surface.Surface):  # if it's an image, then show it
                        surface.blit(encounter['reaction_image_1'], (width_centered, height_centered))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                    return encounter["choices"][0]["health_change"]
                if event.key == pygame.K_2:
                    if isinstance(encounter['reaction_image_2'], pygame.surface.Surface):
                        surface.blit(encounter['reaction_image_2'], (width_centered, height_centered))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                    return encounter["choices"][1]["health_change"]
                if event.key == pygame.K_3:
                    if isinstance(encounter['reaction_image_3'], pygame.surface.Surface):
                        surface.blit(encounter['reaction_image_3'], (width_centered, height_centered))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                    return encounter["choices"][2]["health_change"]

def bad_ending(username): # DYSENTERY
    surface.fill(BLACK)
    display_text(surface, f"You, {username} have died of dysentery.", 100, 300)
    pygame.display.flip()
    pygame.time.delay(5000) # is five seconds enough?

def good_ending(username):
    surface.fill((0, 0, 0))
    display_text(surface, f"You, {username}, have reached Oregon!", 100, 300)
    pygame.display.flip()
    pygame.time.delay(1000)  # DEBUG: LOWER IF NEEDED FOR TESTING

def start_the_game(username):
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
            good_ending(username) if health > 0 else bad_ending()
            break

        result = encounter_choice(encounters[encounter_index]) # grab result from encounter
        health += result
        encounter_index += 1

        if health <= 0: # if you die
            running = False
            bad_ending(username)
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
    name_input = mainmenu.add.text_input('Name: ', default='username', maxchar=25)
    mainmenu.add.button('Play', lambda: start_the_game(name_input.get_value()))
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
