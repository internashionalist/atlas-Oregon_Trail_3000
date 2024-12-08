import pygame
import pygame_menu
from pygame_menu import themes
import sys
import os

os.environ["SDL_VIDEODRIVER"] = "x11"
os.environ["SDL_OPENGL"] = "0"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
os.environ["MESA_LOADER_DRIVER_OVERRIDE"] = "swrast"
os.environ["DISPLAY"] = "host.docker.internal:2"  # comment out for running outside docker
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-dir"
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
        "text": "A swarm of Lost Souls surrounds your vehicle, screeching and blazing with fiery auras.",
        "choices": [
        {
            "text": "Fight with your handy shotgun (-15 health, -3 ammo, +3 supplies)",
            "health_change": -15,
            "ammo_change": -3,
            "fuel_change": 0,
            "supply_change": +3
        },
        {
            "text": "Step on the gas (-2 fuel, -5 health)",
            "health_change": -5,
            "ammo_change": 0,
            "fuel_change": -2,
            "supply_change": 0
        },
        {
            "text": "Make an offering to the lost (-2 supplies, +1 ammo)",
            "health_change": 0,
            "ammo_change": +1,
            "fuel_change": 0,
            "supply_change": -2
        }
    ],
    "flavor_texts": [
        "You blast the Lost Souls away, but at the cost of precious ammo and health.",
        "You speed through the ghostly swarm, but not without a few scratches and some lost fuel.",
        "You offer the Lost Souls some of your supplies, and they let you pass without incident."
    ],
    "background_image": pygame.image.load("assets/Lost_Souls.jpg"),
    "reaction_image_1": pygame.image.load("assets/Lost_Souls_Fight.jpg"),
    "reaction_image_2": pygame.image.load("assets/Lost_Souls_Flee.jpg"),
    "reaction_image_3": pygame.image.load("assets/Lost_Souls_Offering.jpg")
    },
    {
        "text": "A river of molten lava blocks your path, glowing with intense heat.",
        "choices": [
        {
            "text": "Build a makeshift bridge (-10 health, -4 supplies)",
            "health_change": -10,
            "ammo_change": 0,
            "fuel_change": 0,
            "supply_change": -4
        },
        {
            "text": "Endure the searing heat and power through (-30 health, -2 fuel)",
            "health_change": -30,
            "ammo_change": 0,
            "fuel_change": -2,
            "supply_change": 0
        },
        {
            "text": "Find an alternate route (-4 fuel, -2 supplies)",
            "health_change": 0,
            "ammo_change": 0,
            "fuel_change": -4,
            "supply_change": -2
        }
    ],
    "flavor_texts": [
        "You build a bridge out of scrap metal and cross safely, but not without a few burns and bruises.",
        "You power through the lava, but not without some serious burns and health loss.",
        "You find an alternate route, but not without losing some fuel and supplies."
    ],
    "background_image": pygame.image.load("assets/Lava_River.jpg"),
    "reaction_image_1": pygame.image.load("assets/Lava_River_Bridge.jpg"),
    "reaction_image_2": pygame.image.load("assets/Lava_River_Through.jpg"),
    "reaction_image_3": pygame.image.load("assets/Lava_River_Alternate.jpg")
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
    draw_resource_bar(screen, 50, 50, 300, 30, health, 100, GREEN)
    display_text(screen, "Health", 360, 50)
    draw_resource_bar(screen, 50, 100, 300, 30, ammo, 50, BLUE)
    display_text(screen, "Ammo", 360, 100)
    draw_resource_bar(screen, 50, 150, 300, 30, fuel, 20, ORANGE)
    display_text(screen, "Fuel", 360, 150)
    draw_resource_bar(screen, 50, 200, 300, 30, supplies, 10, GREEN)
    display_text(screen, "Supplies", 360, 200)

def scale_image(image, screen_width, screen_height):
    # scales an image to the current screen height
    return pygame.transform.scale(image, (screen_width, screen_height))

def encounter_choice(encounter, health, ammo, fuel, supplies):
    surface.fill(BLACK)
    current_screen_width, current_screen_height = surface.get_size()
    resized_encounter_image = scale_image(encounter['background_image'], current_screen_width, current_screen_height)
    surface.blit(resized_encounter_image, (0, 0))

    text_background_rect = pygame.Rect(50, 250, screen_width - 100, 300)
    pygame.draw.rect(surface, BLACK, text_background_rect)

    display_text(surface, encounter["text"] + '\n', 100, 300)

    for i, choice in enumerate(encounter["choices"]):
        display_text(surface, f"{i + 1}: {choice['text']}", 100, 350 + i * 50)
    pygame.display.flip()

    resource_display(surface, health, ammo, fuel, supplies)
    pygame.display.flip()

    while True:  # main game loop with choice selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                choice_index = event.key - pygame.K_1
                reaction_image = encounter[f"reaction_image_{choice_index + 1}"]
                flavor_text = encounter["flavor_texts"][choice_index]

                surface.blit(reaction_image, (0, 0))
                pygame.draw.rect(surface, BLACK, pygame.Rect(50, screen_height - 150, screen_width - 100, 100))
                display_text(surface, flavor_text, 60, screen_height - 120)
                resource_display(surface, health, ammo, fuel, supplies)
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
    pygame.time.delay(5000)  # DEBUG: LOWER IF NEEDED FOR TESTING

def start_the_game(username):
    health, ammo, fuel, supplies = 100, 50, 20, 10
    encounter_index = 0

    for encounter in encounters:
        health, ammo, fuel, supplies = encounter_choice(encounter, health, ammo, fuel, supplies)
        if health <= 0 or ammo <= 0 or fuel <= 0 or supplies <= 0:
            bad_ending(username)
            return
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
