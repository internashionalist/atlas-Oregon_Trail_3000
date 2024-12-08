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
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
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

def draw_resource_bar(screen, x, y, width, height, current_value, max_value, color):
    pygame.draw.rect(screen, RED, (x, y, width, height))
    fill_width = int((current_value / max_value) * width)
    pygame.draw.rect(screen, color, (x, y, fill_width, height))
    resource_text = f"{current_value}/{max_value}"
    text_surface = font.render(resource_text, True, BLACK)
    text_x = x + width // 2 - text_surface.get_width() // 2
    text_y = y + height // 2 - text_surface.get_height() // 2
    screen.blit(text_surface, (text_x, text_y))

def resource_display(screen, health, ammo, fuel, supplies):
    draw_resource_bar(screen, 50, 50, 300, 30, health, 100, GREEN)  # Health
    display_text(screen, "Health", 360, 50)
    draw_resource_bar(screen, 50, 100, 300, 30, ammo, 50, BLUE)     # Ammo
    display_text(screen, "Ammo", 360, 100)
    draw_resource_bar(screen, 50, 150, 300, 30, fuel, 20, ORANGE)   # Fuel
    display_text(screen, "Fuel", 360, 150)
    draw_resource_bar(screen, 50, 200, 300, 30, supplies, 10, GREEN)  # Supplies
    display_text(screen, "Supplies", 360, 200)

def scale_image(image, screen_width, screen_height):
    # scales an image to the current screen height
    return pygame.transform.scale(image, (screen_width, screen_height))

def encounter_choice(encounter, health, ammo, fuel, supplies):
    surface.fill(BLACK)
    current_screen_width, current_screen_height = surface.get_size()
    resized_encounter_image = scale_image(encounter['background_image'], current_screen_width, current_screen_height)
    surface.blit(resized_encounter_image, (0, 0))
    display_text(surface, encounter["text"] + '\n', 100, 300)

    for i, choice in enumerate(encounter["choices"]):
        display_text(surface, f"{i + 1}: {choice['text']}", 100, 350 + i * 50)

    pygame.display.flip()

    while True:  # main game loop with choice selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # key presses
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    choice_index = event.key - pygame.K_1  # map keys to index
                    reaction_image_key = f"reaction_image_{choice_index + 1}"
                    
                    if reaction_image_key in encounter and isinstance(encounter[reaction_image_key], pygame.surface.Surface):
                        current_screen_width, current_screen_height = surface.get_size()
                        reaction_image = encounter[reaction_image_key]
                        width_centered = (current_screen_width - reaction_image.get_width()) / 2
                        height_centered = (current_screen_height - reaction_image.get_height()) / 2

                        surface.blit(reaction_image, (width_centered, height_centered))
                        pygame.display.flip()
                        pygame.time.delay(3000)

                    choice = encounter["choices"][choice_index]
                    health += choice.get("health_change", 0)
                    ammo += choice.get("ammo_change", 0)
                    fuel += choice.get("fuel_change", 0)
                    supplies += choice.get("supply_change", 0)

                return health, ammo, fuel, supplies

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
    health, ammo, fuel, supplies = 100, 50, 20, 10
    encounter_index = 0

    while encounter_index < len(encounters):
        health, ammo, fuel, supplies = encounter_choice(
            encounters[encounter_index], health, ammo, fuel, supplies
        )
        if health <= 0 or ammo <= 0 or fuel <= 0 or supplies <= 0:
            bad_ending(username)
            return

        encounter_index += 1
        surface.fill(BLACK)
        resource_display(surface, health, ammo, fuel, supplies)
        pygame.display.flip()

    good_ending(username)


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
