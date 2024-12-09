import pygame
import pygame_menu
from pygame_menu import themes
import sys
import os

os.environ["SDL_OPENGL"] = "0"
os.environ["SDL_VIDEODRIVER"] = "x11"
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
os.environ["MESA_LOADER_DRIVER_OVERRIDE"] = "swrast"
#os.environ["DISPLAY"] = "host.docker.internal:0"  # comment out for running outside docker
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-dir"
os.environ["SDL_AUDIODRIVER"] = "dummy"


pygame.init() # start 'er up
clock = pygame.time.Clock()
username = ''

screen_width, screen_height = 1920, 1080
surface = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.FULLSCREEN)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

def load_and_scale_image(image_path, screen_width, screen_height):
    raw_image = pygame.image.load(image_path)
    return pygame.transform.scale(raw_image, (screen_width, screen_height))

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
        "background_image": load_and_scale_image("assets/Lost_Souls.jpg", screen_width, screen_height),
        "reaction_image_1": load_and_scale_image("assets/Lost_Souls_Fight.jpg", screen_width, screen_height),
        "reaction_image_2": load_and_scale_image("assets/Lost_Souls_Flee.jpg", screen_width, screen_height),
        "reaction_image_3": load_and_scale_image("assets/Lost_Souls_Offering.jpg", screen_width, screen_height)
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
        "background_image": load_and_scale_image("assets/Lava_River.jpg", screen_width, screen_height),
        "reaction_image_1": load_and_scale_image("assets/Lava_River_Bridge.jpg", screen_width, screen_height),
        "reaction_image_2": load_and_scale_image("assets/Lava_River_Through.jpg", screen_width, screen_height),
        "reaction_image_3": load_and_scale_image("assets/Lava_River_Alternate.jpg", screen_width, screen_height)
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
        "background_image": load_and_scale_image("assets/Marauders.jpg", screen_width, screen_height),
        "reaction_image_1": load_and_scale_image("assets/Marauders_Fight.jpg", screen_width, screen_height),
        "reaction_image_2": load_and_scale_image("assets/Marauders_Fuel.jpg", screen_width, screen_height),
        "reaction_image_3": load_and_scale_image("assets/Marauders_Supplies.jpg", screen_width, screen_height)
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
    "background_image": load_and_scale_image("assets/Storm.jpg", screen_width, screen_height),
    "reaction_image_1": load_and_scale_image("assets/Storm_Endure.jpg", screen_width, screen_height),
    "reaction_image_2": load_and_scale_image("assets/Storm_Through.jpg", screen_width, screen_height),
    "reaction_image_3": load_and_scale_image("assets/Storm_Around.jpg", screen_width, screen_height)
    },
    {
        "text": "An Archdevil wielding a massive flaming sword blocks your path. Its eyes glow with malice as it dares your party to approach.",
        "choices": [
            {
                "text": "Engage in an epic all-out battle (-50 health, -8 ammo, -2 fuel)",
                "health_change": -50,
                "ammo_change": -8,
                "fuel_change": -2,
                "supply_change": 0
            },
            {
                "text": "Launch fuel cells as explosive countermeasures (-20 health, -10 fuel)",
                "health_change": -20,
                "ammo_change": 0,
                "fuel_change": -10,
                "supply_change": 0
            },
            {
                "text": "Attempt to negotiate with the Archdevil (-5 fuel, -5 supplies)",
                "health_change": 0,
                "ammo_change": 0,
                "fuel_change": -5,
                "supply_change": -5
            }
        ],
        "flavor_texts": [
            "You unleash everything you have against the Archdevil, suffering terrible wounds but collecting a hoard of supplies.",
            "You cleverly use your fuel cells to blow the Archdevil back to Hell, restoring your morale.",
            "You offer a valuable tribute, and the Archdevil begrudgingly lets you pass, improving your spirits."
        ],
        "background_image": load_and_scale_image("assets/Archdevil.jpg", screen_width, screen_height),
        "reaction_image_1": load_and_scale_image("assets/Archdevil_Battle.jpg", screen_width, screen_height),
        "reaction_image_2": load_and_scale_image("assets/Archdevil_Fuel.jpg", screen_width, screen_height),
        "reaction_image_3": load_and_scale_image("assets/Archdevil_Negotiate.jpg", screen_width, screen_height)
    }
]
def word_wrap(text, max):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        temp_line = current_line + " " + word if current_line else word
        width, _ = font.size(temp_line)
        if width <= max:
            current_line = temp_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def display_text(screen, text, x, y):
    lines = word_wrap(text, screen_width - 50)
    line_height = font.get_height()
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, GREEN)
        screen.blit(rendered_text, (x, y + i * line_height))

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

def intro():
    """This is the intro after main menu"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        surface.fill(BLACK)
        try:
            with open("dialogue.txt", "r") as file:
                content = file.read()
            display_text(surface, content, 0, 0)
        except FileNotFoundError:
            print("Error: file not found")
        pygame.display.update()
        pygame.time.Clock().tick(60)

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

def dysentery_ending(username): # DYSENTERY
    surface.fill(BLACK)
    dysentery_image = load_and_scale_image("assets/Dysentery.jpg", screen_width, screen_height)
    surface.blit(dysentery_image, (0, 0))
    display_text(surface, f"You, {username} have died of dysentery.", 100, 300)
    pygame.display.flip()
    pygame.time.delay(5000)

def ammo_ending():
    surface.fill(BLACK)
    ammo_image = load_and_scale_image("assets/Ammo_Ending.jpg", screen_width, screen_height)
    surface.blit(ammo_image, (0, 0))
    display_text(surface, "Overwhelmed and defenseless...", 100, 300)
    display_text(surface, "Without ammo, you were unable to fend off the dangers of Mars.", 100, 350)
    pygame.display.flip()
    pygame.time.delay(5000)

def fuel_ending():
    surface.fill(BLACK)
    fuel_image = load_and_scale_image("assets/Fuel_Ending.jpg", screen_width, screen_height)
    surface.blit(fuel_image, (0, 0))
    display_text(surface, "Stranded and without options...", 100, 300)
    display_text(surface, "Out of fuel, you were unable to continue your journey.", 100, 350)
    pygame.display.flip()
    pygame.time.delay(5000)

def supplies_ending():
    surface.fill(BLACK)
    supplies_image = load_and_scale_image("assets/Supplies_Ending.jpg", screen_width, screen_height)
    surface.blit(supplies_image, (0, 0))
    display_text(surface, "Starving and desperate...", 100, 300)
    display_text(surface, "Without supplies, survival was impossible.", 100, 350)
    pygame.display.flip()
    pygame.time.delay(5000)

def good_ending(username):
    surface.fill(BLACK)
    good_ending_image = load_and_scale_image("assets/Good_Ending.jpg", screen_width, screen_height)
    surface.blit(good_ending_image, (0, 0))
    display_text(surface, "Congratulations!", 100, 300)
    display_text(surface, f"You, {username}, have reached New Oregon!", 100, 350)
    pygame.display.flip()
    pygame.time.delay(5000)

def start_the_game(username):
    intro()
    health, ammo, fuel, supplies = 100, 50, 20, 10
    encounter_index = 0

    for encounter in encounters:
        health, ammo, fuel, supplies = encounter_choice(encounter, health, ammo, fuel, supplies)
        if health <= 0:
            dysentery_ending(username)
            return
        elif ammo <= 0:
            ammo_ending()
            return
        elif fuel <= 0:
            fuel_ending()
            return
        elif supplies <= 0:
            supplies_ending()
            return

        resource_display(surface, health, ammo, fuel, supplies)
        pygame.display.flip()
        clock.tick(60)
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
    mainmenu.add.button('Intro', lambda: intro())
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mainmenu.update(events)
        mainmenu.draw(surface)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    mainmenu()
    pygame.quit()
