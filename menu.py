#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random
from Pokemon_pokedex import PokemonDex
from Pokemon_pokedex import Pokedex
import Pokemon_pokedex

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Mon-Poke")
screen = pygame.display.set_mode((380, 350), 0, 32)

font = pygame.font.Font('RBYGSC.ttf', 16)
font1 = pygame.font.Font('RBYGSC.ttf', 12)

color1, color2 = (88, 120, 184), (42, 61, 99)

global refresh 
refresh = False

def type_format(input):
    type_abb = {'normal':'NRM', 'fire':'FIR', 'water':'WTR', 'grass':'GRA', 'electric':'ELE', 'ice':'ICE', 'fighting':'FGT', 'poison':'POI', 'ground':'GRD', 'flying':'FLY', 'psychic':'PSY', 'bug':'BUG', 'rock':'ROC', 'ghost':'GST', 'dark':'DAR', 'dragon':'DRG', 'steel':'STL', 'fairy':'FAI', 'uwu':'uwu'}
    output = ''
    if "," in input:
        input1, input2 = input.split(',')
        output = f'{str(type_abb[input1])},{str(type_abb[input2])}'
        num = 2
    else:
        output = f'{str(type_abb[input])}'
        num = 1
    return output, num

def slice_pokes(dictionary, current_index):
    slice_return = []
    length = len(dictionary)
    if (current_index + 3 < length):
        numbers = 4
    else:
        numbers = length - current_index

    for i in range(numbers):
        slice_return.append(current_index + i)
    return slice_return, numbers

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    click = False
    while True:
        screen.fill((39, 43, 51))
        draw_text("main menu", font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        pygame.draw.rect(screen, color1, button_1)
        pygame.draw.rect(screen, color1, button_2)

        draw_text("Pokedex", font, (255, 255, 255), screen, 75, 120)
        draw_text("Catch  More", font, (255, 255, 255), screen, 75, 220)
        
        
        if button_1.collidepoint((mx, my)):
            if click:
                pokedex_menu()

        if button_2.collidepoint((mx, my)):
            if click:
                return

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def pokedex_menu():
    global refresh
    print(refresh)
    click = False
    temp_pokedex = Pokedex()
    temp_pokedex.set_list("save.txt")
    dic_pokemons = temp_pokedex.get_list()

    running = True
    display_boxes = False
    current_index = 0
    while running:
        if(refresh):
            print('bruh')
            temp_pokedex = Pokedex()
            temp_pokedex.set_list("save.txt")
            dic_pokemons = temp_pokedex.get_list()
            refresh = False


        screen.fill((39, 43, 51))
        mx, my = pygame.mouse.get_pos()
        slice_list, number = slice_pokes(dic_pokemons, current_index)

        draw_text('Pokedex', font, (225, 255, 255), screen, 15, 10)

        # Shows the user what box they're on in the top right corner.
        if current_index // 4 + 1 < 10:
            box_button = pygame.Rect(310, 10, 75, 25)
            pygame.draw.rect(screen, color1, box_button)
            draw_text('box '+str(current_index // 4 + 1), font, (225, 255, 255), screen, 315, 12)
        else:
            box_button = pygame.Rect(300, 10, 85, 25)
            pygame.draw.rect(screen, color1, box_button)
            draw_text('box '+str(current_index // 4 + 1), font, (225, 255, 255), screen, 305, 12)

        # For the user clicking to see box options to change their box.
        if box_button.collidepoint((mx, my)):
            if click:
                display_boxes = not display_boxes
        if display_boxes:
            quick_change_buttons = display_box_options(current_index, temp_pokedex)

            # Goes through each button and sees if it was clicked.
            for i in range(len(quick_change_buttons)):
                if quick_change_buttons[i].collidepoint((mx, my)):
                    if click:

                        # Checks the index compared to which button was clicked
                        # Subtracting 2 since index 2 is the middle for no change.
                        change = i - 2

                        # Changes the index depending on the button which was clicked.
                        for k in range(abs(change)):

                            current_index += int((4 * change / abs(change)))
                            if current_index > temp_pokedex.get_list_length():
                                current_index = 0
                            if current_index < 0:
                                current_index = temp_pokedex.get_list_length() // 4 * 4

        button_1 = pygame.Rect(15, 50, 280, 50)
        button_2 = pygame.Rect(15, 125, 280, 50)
        button_3 = pygame.Rect(15, 200, 280, 50)
        button_4 = pygame.Rect(15, 275, 280, 50)
        button_5 = pygame.Rect(321, 217, 50, 25)
        button_6 = pygame.Rect(321, 270, 50, 25)

        pygame.draw.rect(screen, color1, button_1)
        image1 = pygame.image.load(f'pokemon_pics/{dic_pokemons[f"poke_{slice_list[0]}"].get_species()}_far.png')
        screen.blit(image1, (255, 45))
        draw_text(dic_pokemons[f'poke_{slice_list[0]}'].get_species().title(), font, (255, 255, 255), screen, 20, 55)
        draw_text('Lv. '+str(dic_pokemons[f'poke_{slice_list[0]}'].get_level()), font, (255, 255, 255), screen, 20, 80)

        if(number >= 2):
            pygame.draw.rect(screen, color1, button_2)
            image2 = pygame.image.load(f'pokemon_pics/{dic_pokemons[f"poke_{slice_list[1]}"].get_species()}_far.png')
            screen.blit(image2, (255, 120))
            draw_text(dic_pokemons[f'poke_{slice_list[1]}'].get_species().title(), font, (255, 255, 255), screen, 20, 130)
            draw_text('Lv. '+str(dic_pokemons[f'poke_{slice_list[1]}'].get_level()), font, (255, 255, 255), screen, 20, 155)

        if(number >= 3):
            pygame.draw.rect(screen, color1, button_3)
            image3 = pygame.image.load(f'pokemon_pics/{dic_pokemons[f"poke_{slice_list[2]}"].get_species()}_far.png')
            screen.blit(image3, (255, 195))
            draw_text(dic_pokemons[f'poke_{slice_list[2]}'].get_species().title(), font, (255, 255, 255), screen, 20, 205)
            draw_text('Lv. '+str(dic_pokemons[f'poke_{slice_list[2]}'].get_level()), font, (255, 255, 255), screen, 20, 230)

        if(number >= 4):
            pygame.draw.rect(screen, color1, button_4)
            image4 = pygame.image.load(f'pokemon_pics/{dic_pokemons[f"poke_{slice_list[3]}"].get_species()}_far.png')
            screen.blit(image4, (255, 270))
            draw_text(dic_pokemons[f'poke_{slice_list[3]}'].get_species().title(), font, (255, 255, 255), screen, 20, 280)
            draw_text('Lv. '+str(dic_pokemons[f'poke_{slice_list[3]}'].get_level()), font, (255, 255, 255), screen, 20, 305)

        # Draw buttons for going forward and backward.
        pygame.draw.rect(screen, color2, button_5)
        pygame.draw.rect(screen, color2, button_6)
        draw_text('fwd', font, (255, 255, 255), screen, 326, 217)
        draw_text('bwd', font, (255, 255, 255), screen, 326, 270)

        # Button logic when they're clicked.
        if button_1.collidepoint((mx, my)):
            if click:
                pokedex(f'poke_{slice_list[0]}')

        if button_2.collidepoint((mx, my))  and number >= 2:
            if click:
                pokedex(f'poke_{slice_list[1]}')
        
        if button_3.collidepoint((mx, my))  and number >= 3:
            if click:
                pokedex(f'poke_{slice_list[2]}')
        
        if button_4.collidepoint((mx, my))  and number >= 4:
            if click:
                pokedex(f'poke_{slice_list[3]}')

        if button_5.collidepoint((mx, my)):
            if click:
                current_index += 4
                if current_index > temp_pokedex.get_list_length():
                    current_index = 0

        if button_6.collidepoint((mx, my)):
            if click:
                current_index -= 4
                if current_index < 0:
                    current_index = temp_pokedex.get_list_length() // 4 * 4

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def pokedex(id_tag):

    global refresh
    # image = pygame.image.load(image_name)

    # species, excess = image_name.strip(".png").split("_")

    # species = pokemon_name1.title()

    temp_pokedex = Pokedex()
    temp_pokedex.set_list("save.txt")
    dic_pokemon = temp_pokedex.get_list()
    name, species, typ, level, CP, stats, IV, date, difficulty = dic_pokemon[id_tag].return_details()


    pygame.display.set_caption(f"Summary - {species}")

    typ_reform, num = type_format(typ)

    image = pygame.image.load(f'pokemon_pics/{species}_close.png')

    # temp_pokemon = PokemonDex(pokemon_name1, "Dragonite")
    # name, species, type, level, CP, stats, IV, date = temp_pokemon.return_details()

    running = True
    click = False
    while running:
        
        mx, my = pygame.mouse.get_pos()
        screen.fill((39, 43, 51))

        """drawing pokemon image and a border around it"""
        screen.blit(image, (20, 60))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10.5, 50, 140, 140), 2)

        """pokemon name text and the box it's in"""
        pygame.draw.polygon(
            screen, color1, ((10, 20), (120, 20), (140, 50), (10, 50))
        )
        draw_text(f"{name}", font, (255, 255, 255), screen, 20, 23)

        """pokemon level text and the box it's in"""
        pygame.draw.polygon(
            screen, color2, ((120, 20), (220, 20), (220, 50), (140, 50))
        )
        draw_text(f"Lv.{str(level)}", font, (255, 255, 255), screen, 150, 20)

        """summary screen"""
        pygame.draw.rect(screen, color2, pygame.Rect(170, 70, 201, 30))
        pygame.draw.polygon(
            screen, color1, ((170, 100), (370, 100), (370, 170), (215, 170))
        )

        # draw_text("Summary", font, (255, 255, 255), screen, 240, 75)
        if(len(species) > 7):
            draw_text(f"Species: {species.title()}", font1, (255, 255, 255), screen, 186, 75)
        else:
            draw_text(f"Species: {species.title()}", font, (255, 255, 255), screen, 185, 72)
        if num == 2:
            draw_text(f"Type: {typ_reform}", font, (255, 255, 255), screen, 205, 110)
        elif num == 1:
            draw_text(f"Type: {typ_reform}", font, (255, 255, 255), screen, 235, 110)
        draw_text(f"CP: {int(float(CP))}", font, (255, 255, 255), screen, 240, 140)
        

        """stats and IVs"""
        pygame.draw.rect(screen, color2, pygame.Rect(10, 193, 370 - 10, 120))
        draw_text(
            f"STATS                        IVs: {round(IV,2)}",
            font,
            (255, 255, 255),
            screen,
            20,
            198,
        )
        draw_text("ATK", font, (255, 255, 255), screen, 20, 230)
        draw_text("DEF", font, (255, 255, 255), screen, 20, 255)
        draw_text("STA", font, (255, 255, 255), screen, 20, 280)
        
        """power up & release"""
        button_1 = pygame.Rect(10, 320, 120, 25)
        pygame.draw.rect(screen, color1, button_1)
        draw_text("POWER UP", font, (255, 255, 255), screen, 15, 322)

        button_2 = pygame.Rect(145, 320, 120, 25)
        pygame.draw.rect(screen, color1, button_2)
        draw_text("RELEASE", font, (255, 255, 255), screen, 150, 322)

        if button_1.collidepoint((mx, my)):
            if click:
                dic_pokemon[id_tag].power_up()
                Pokemon_pokedex.export_pokes(dic_pokemon)
                dic_pokemon = temp_pokedex.get_list()
                name, species, typ, level, CP, stats, IV, date, difficulty = dic_pokemon[id_tag].return_details()
        
        if button_2.collidepoint((mx, my)):
            if click:
                temp_pokedex.release(name)
                refresh = True
                running = False

    

        # repeating boxes for however many IVs they have
        for j in range(3):
            for i in range(stats[j]):
                pygame.draw.rect(
                    screen,
                    color1,
                    pygame.Rect(70 + i * 20, 240 + j * 25, 7, 7),
                )
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


# Displays options for boxes that can be clicked on to go quicly from one box to another.
def display_box_options(current_index, temp_pokedex):

    # Covers up the normal box button.
    box_button = pygame.Rect(300, 10, 85, 25)
    pygame.draw.rect(screen, (39, 43, 51), box_button)

    # Makes it so that the box numbers start at 2 before the current.
    for i in range(2):
        current_index -= 4
        if current_index < 0:
            current_index = temp_pokedex.get_list_length() // 4 * 4

    # Sets parameters for boxes, as well as box for clicking back to get rid of options.
    box_height = 25
    back_box = pygame.Rect(310, 10, 75, box_height)
    pygame.draw.rect(screen, color1, back_box)
    buttons = [pygame.Rect(345, 10 + (i + 1) * box_height, 35, box_height) for i in range(5)]

    # Create buttons to go on screen with outlines.
    for button in buttons:
        pygame.draw.rect(screen, color1, button)
        pygame.draw.rect(screen, (0, 0, 0), button, 1)

    draw_text('back', font, (225, 255, 255), screen, 320, 12)

    # Draws text on buttons.
    for i in range(5):
        draw_text(str(current_index // 4 + 1), font, (225, 255, 255), screen, 350, 12 + (i + 1) * box_height)
        current_index += 4
        if current_index > temp_pokedex.get_list_length():
            current_index = 0

    '''
    current_index += 4
                if current_index > temp_pokedex.get_list_length():
                    current_index = 0
    current_index -= 4
                if current_index < 0:
                    current_index = temp_pokedex.get_list_length() // 4 * 4
                    
        if current_index // 4 + 1 < 10:
        else:
            box_button = pygame.Rect(300, 10, 85, 25)
            pygame.draw.rect(screen, color1, box_button)
            draw_text('box '+str(current_index // 4 + 1), font, (225, 255, 255), screen, 305, 12)
    '''

    return buttons


main_menu()
