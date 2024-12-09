import pygame
import pygame_menu
from pygame_menu import themes
import sys
import os

os.environ["SDL_OPENGL"] = "0"
os.environ["SDL_VIDEODRIVER"] = "x11"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
os.environ["MESA_LOADER_DRIVER_OVERRIDE"] = "swrast"
os.environ["DISPLAY"] = "host.docker.internal:0"  # comment out for running outside docker
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
        "text": "A swarm of Lost Souls surrounds your rover, screeching and blazing with fiery auras.",
        "choices": [
            {
                "text": "Fight with your handy shotgun (-15 health, -3 ammo, +3 supplies)",
                "health_change": -15,
                "ammo_change": -3,
                "fuel_change": 0,
                "supply_change": +3
            },
            {
                "text": "Step on the gas (-5 health, -2 fuel, +1 ammo)",
                "health_change": -5,
                "ammo_change": +1,
                "fuel_change": -2,
                "supply_change": 0
            },
            {
                "text": "Make an offering to the lost (-2 supplies, +2 ammo)",
                "health_change": 0,
                "ammo_change": +2,
                "fuel_change": 0,
                "supply_change": -2
            }
        ],
        "flavor_texts": [
            "You blast the Lost Souls away, but at the cost of precious ammo and health.",
            "You speed through the ghostly swarm, but manage to grab a stray ammo clip on your way.",
            "You offer the Lost Souls some of your supplies, and they leave you with extra ammo as thanks."
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
                "text": "Build a makeshift bridge and cross safely (-10 health, -4 supplies, +5 ammo)",
                "health_change": -10,
                "ammo_change": +5,
                "fuel_change": 0,
                "supply_change": -4
            },
            {
                "text": "Endure the searing heat and power through the lava (-30 health, -2 fuel, +2 supplies)",
                "health_change": -30,
                "ammo_change": 0,
                "fuel_change": -2,
                "supply_change": +2
            },
            {
                "text": "Find an alternate route (-4 fuel, -2 supplies, +3 health)",
                "health_change": +3,
                "ammo_change": 0,
                "fuel_change": -4,
                "supply_change": -2
            }
        ],
        "flavor_texts": [
            "You build a bridge out of scrap metal and cross safely, scavenging some ammo along the way.",
            "You power through the lava, but find a hidden supply stash on the other side.",
            "You find an alternate route, avoiding most of the heat and regaining some health."
        ],
        "background_image": pygame.image.load("assets/Lava_River.jpg"),
        "reaction_image_1": pygame.image.load("assets/Lava_River_Bridge.jpg"),
        "reaction_image_2": pygame.image.load("assets/Lava_River_Through.jpg"),
        "reaction_image_3": pygame.image.load("assets/Lava_River_Alternate.jpg")
    },
    {
        "text": "A pack of ravenous Marauders encircles your rover, demanding food and resources.",
        "choices": [
            {
                "text": "Fight them off in a hail of bullets (-20 health, -5 ammo, +8 supplies)",
                "health_change": -20,
                "ammo_change": -5,
                "fuel_change": 0,
                "supply_change": +8
            },
            {
                "text": "Give them some fuel to avoid confrontation (-5 fuel, +3 health)",
                "health_change": +3,
                "ammo_change": 0,
                "fuel_change": -5,
                "supply_change": 0
            },
            {
                "text": "Surrender your supplies to buy your safety (+10 health, -5 supplies)",
                "health_change": +10,
                "ammo_change": 0,
                "fuel_change": 0,
                "supply_change": -5
            }
        ],
        "flavor_texts": [
            "You engage in a brutal fight, taking serious damage but gaining valuable supplies.",
            "You siphon off your fuel to appease the Marauders, feeling a bit relieved afterward.",
            "You hand over your supplies, but your health improves from avoiding a fight."
        ],
        "background_image": pygame.image.load("assets/Marauders.jpg"),
        "reaction_image_1": pygame.image.load("assets/Marauders_Fight.jpg"),
        "reaction_image_2": pygame.image.load("assets/Marauders_Fuel.jpg"),
        "reaction_image_3": pygame.image.load("assets/Marauders_Supplies.jpg")
    },
    {
        "text": "A hellish storm erupts, forcing you to make a quick decision to survive.",
        "choices": [
        {
            "text": "Hunker down and endure the tempest",
            "health_change": -15,
            "ammo_change": 0,
            "fuel_change": 0,
            "supply_change": -3
        },
        {
            "text": "Power through at full throttle",
            "health_change": -10,
            "ammo_change": 0,
            "fuel_change": -6,
            "supply_change": 0
        },
        {
            "text": "Attempt to go around the storm",
            "health_change": 0,
            "ammo_change": 0,
            "fuel_change": 3,
            "supply_change": 2
        }
    ],
    "flavor_texts": [
        "You take shelter for the duration, using precious supplies and sustaining injuries.",
        "You floor it through the storm, burning fuel cells against the winds.",
        "You try to circumnavigate the demonic torrent, spending time and supplies."
    ],
    "background_image": pygame.image.load("assets/Storm.jpg"),
    "reaction_image_1": pygame.image.load("assets/Storm_Endure.jpg"),
    "reaction_image_2": pygame.image.load("assets/Storm_Through.jpg"),
    "reaction_image_3": pygame.image.load("assets/Storm_Around.jpg")
    },
    {
        "text": "An Archdevil wielding a massive flaming sword blocks your path. Its eyes glow with malice as it dares your party to approach.",
        "choices": [
            {
                "text": "Engage in an epic all-out battle (-50 health, -8 ammo, +10 supplies)",
                "health_change": -50,
                "ammo_change": -8,
                "fuel_change": 0,
                "supply_change": +10
            },
            {
                "text": "Launch fuel cells as explosive countermeasures (-10 fuel, +5 health)",
                "health_change": +5,
                "ammo_change": 0,
                "fuel_change": -10,
                "supply_change": 0
            },
            {
                "text": "Attempt to negotiate with the Archdevil (-10 supplies, +10 health)",
                "health_change": +10,
                "ammo_change": 0,
                "fuel_change": 0,
                "supply_change": -10
            }
        ],
        "flavor_texts": [
            "You unleash everything you have against the Archdevil, suffering terrible wounds but collecting a hoard of supplies.",
            "You cleverly use your fuel cells to blow the Archdevil back to Hell, restoring your morale.",
            "You offer a valuable tribute, and the Archdevil begrudgingly lets you pass, improving your spirits."
        ],
        "background_image": pygame.image.load("assets/Archdevil.jpg"),
        "reaction_image_1": pygame.image.load("assets/Archdevil_Battle.jpg"),
        "reaction_image_2": pygame.image.load("assets/Archdevil_Cells.jpg"),
        "reaction_image_3": pygame.image.load("assets/Archdevil_Negotiate.jpg")
    }
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
