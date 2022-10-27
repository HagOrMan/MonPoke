import sys
import pygame
import math
import random

import Pokemon_pokedex
from Pokeball_Class import Pokeball
from Throw_Class import Thrower
from Pokemon_Class import Pokemon
from Star_Class import StarGroup
from Catch_Radius import CatchRadius
from playsound import playsound
from Pokemon_pokedex import Pokedex, PokemonDex
import menu


Color = {
    "lightRed": (255, 20, 20),
    "lightGrey": (200, 200, 200),
    "caught_msg": (50, 150, 220),
    "white": (255, 255, 255),
    "light_green": (87, 253, 104),
    "green": (28, 230, 48),
    "yellow": (244, 250, 70),
    "orange": (255, 164, 60),
    "red": (255, 46, 46),
}

pygame.init()
clock = pygame.time.Clock()
word_font = pygame.font.Font("freesansbold.ttf", 30)
caught_font = pygame.font.Font("freesansbold.ttf", 20)

# Variables for the window.
winWidth, winHeight = 500, 500
win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Mon-Poke")
winColor = pygame.Color("grey12")

background_choice = f'backgrounds/pokemon_background{random.randint(1,6)}.png'
win_background = pygame.image.load(background_choice)

throw_line = Thrower(winWidth, winHeight, (255, 255, 255), 40)

# Variables for the ball.
ball_radius1, ball_radius2 = 30, 10
ball_speed = 15
ball_start_x = winWidth / 2
ball_start_y = winHeight * 0.93

# For the ball moving.
hasPressed = False
ballMoved = False

# Creates a ball to use as well as a pokemon and gets a list of all possible pokemon.
ball = Pokeball(ball_radius1, ball_start_x, ball_start_y)
pokemon = Pokemon(winWidth, winHeight, "Fire")
catch_circle = CatchRadius(
    pokemon.get_pos()[0] + pokemon.get_radius(),
    pokemon.get_pos()[1] + pokemon.get_radius(),
    5,
    5,
    2,
)
poke_list = pokemon.get_poke_list()

# Timer for the pokemon's random jumps.
poke_timer = 0
poke_timer_max = random.randint(100, 500)
poke_change_timer = 0
poke_changed = False
poke_caught = False
num_tries = 0
failed_catch = False
caught_list = []

display_poke = False

# To ensure that the ball isn't red after the pokemon is caught.
ball_caught = False

# Creates the rectangle which shows that the pokemon was caught.
caught_rect = pygame.rect.Rect((0, winHeight - 70.0, winWidth, 50))

pokedex = Pokedex()
pokedex.set_list('save.txt')


# Draws the message showing which pokemon was caught.
def draw_caught_msg():
    an_or_a = "a"
    if (
        pokemon.get_name()[0] == "A"
        or pokemon.get_name()[0] == "E"
        or pokemon.get_name()[0] == "I"
        or pokemon.get_name()[0] == "O"
        or pokemon.get_name()[0] == "U"
    ):
        an_or_a = "an"
    caught_text = "You caught " + an_or_a + " " + pokemon.get_name() + "!"
    caught_msg = word_font.render(caught_text, False, Color["white"])
    pygame.draw.rect(win, Color["caught_msg"], caught_rect)
    win.blit(caught_msg, (winWidth / 5, winHeight - 60))


# Creates the animation when a pokemon is caught.
def caught_poke():
    global ball_caught, num_tries, failed_catch

    # Has the ball bounce off of the pokemon if it was caught, also saves if it was a nice/great/excellent throw.
    catch_modifier = ball.bounce_off(
        win,
        Color,
        win_background,
        pokemon,
        clock,
        poke_caught and not ball_caught,
        catch_circle,
    )

    # Creates a circle expanding animation to show the pokemon being caught.
    circle_radius = 1
    poke_x, poke_y = pokemon.get_pos()
    poke_x += pokemon.get_radius()
    poke_y += pokemon.get_radius()

    # Has a circle expand quickly as an animation for the pokemon being caught.
    while circle_radius < pokemon.get_radius() * 1.2:
        pokemon.draw_self(win)
        pygame.draw.circle(win, (255, 255, 255), (poke_x, poke_y), circle_radius)
        circle_radius += 3
        ball.draw_ball(win, Color, poke_caught and not ball_caught)
        pygame.display.flip()
        pygame.time.delay(15)

        # Makes the pokemon invisible once the circle is big enough.
        if circle_radius > pokemon.get_radius() * 0.9:
            pokemon.set_visibility(False)

    win.blit(win_background, (0, 0))
    ball.draw_ball(win, Color, poke_caught and not ball_caught)
    pygame.display.flip()
    ball.draw_ball(win, Color, poke_caught and not ball_caught)

    # Makes the ball bounce a couple times before catching the pokemon for good.
    for bounce in range(3):

        # Logic for having the pokemon not be caught every once in a while.
        # Higher chance if they had a better throw, lower for the greater the pokemon difficulty.
        random_catch = random.randint(0, 7 - catch_modifier + decide_difficulty())
        if not failed_catch:
            if random_catch == 0:
                if num_tries < 3:
                    num_tries += 1

                    # Resets the pokemon because it wasn't caught and leaves the method.
                    reset_poke()

                    # A sound of amazement after catching the pokemon.
                    playsound("kidding_me.mp3")
                    return
                # Resets the num tries if they've failed too many times and should catch the pokemon this time.
                else:
                    num_tries = 0
                    failed_catch = True

        pygame.time.delay(1000)
        for i in range(5):
            ball.y -= 2

            win.blit(win_background, (0, 0))
            ball.draw_ball(win, Color, poke_caught and not ball_caught)
            pygame.display.flip()
            pygame.time.delay(30)
        for i in range(5):
            ball.y += 2

            win.blit(win_background, (0, 0))
            ball.draw_ball(win, Color, poke_caught and not ball_caught)
            pygame.display.flip()
            pygame.time.delay(30)

    ball_caught = True

    pygame.time.delay(1000)
    # Has stars appear around the ball once it is caught.
    stars = StarGroup(ball)
    win.blit(win_background, (0, 0))
    ball.draw_ball(win, Color, poke_caught and not ball_caught)
    stars.draw_self(win)
    pygame.display.flip()

    # A sound of amazement after catching the pokemon.
    playsound("wow.mp3")

    # Draws the game with the stars gone.
    win.blit(win_background, (0, 0))
    ball.draw_ball(win, Color, poke_caught and not ball_caught)
    pygame.display.flip()

    caught_list.append(pokemon.get_name())

    # Adds the caught pokemon to the pokedex.
    add_poke_to_dex()

    # playsound('/Users/khagy/PycharmProjects/pokemonTest/lets_get_it_on.mp3')


# Asks the user to enter a nickname for their pokemon.
def add_poke_to_dex():
    # nickname = input("Enter a nickname for your pokemon, or press enter to keep their normal name: ")

    # Saves the pokemon that was just caught to the save file.
    pokedex.get_type_list()
    pokedex.add_pokemon(pokemon.get_name(), decide_difficulty())  # Add the nickname to add pokemon when baoze adds.
    pokemons = pokedex.get_list()
    Pokemon_pokedex.export_pokes(pokemons)


# Resets the pokemon if it is not caught.
def reset_poke():
    global poke_caught, ball_caught
    poke_caught = False
    ball_caught = False

    # Animation to have the pokemon come out of the ball.
    circle_radius = 1
    poke_x, poke_y = pokemon.get_pos()
    poke_x += pokemon.get_radius()
    poke_y += pokemon.get_radius()

    # Has a circle expand quickly as an animation for the pokemon being released.
    while circle_radius < pokemon.get_radius() * 1.2:
        pokemon.draw_self(win)
        pygame.draw.circle(win, (240, 240, 240), (poke_x, poke_y), circle_radius)
        circle_radius += 3
        ball.draw_ball(win, Color, poke_caught and not ball_caught)
        pygame.display.flip()
        pygame.time.delay(10)

        # Makes the pokemon visible once the circle is big enough.
        if circle_radius > pokemon.get_radius() * 0.9:
            pokemon.set_visibility(True)

    win.blit(win_background, (0, 0))
    ball.draw_ball(win, Color, poke_caught and not ball_caught)
    pokemon.draw_self(win)
    pygame.display.flip()
    ball.draw_ball(win, Color, poke_caught and not ball_caught)
    pokemon.draw_self(win)


# Displays the pokemon caught.
def display_caught():
    win.fill(winColor)

    caught_text1 = "Pokemon Caught"
    caught_text2 = "This Session:"

    if len(caught_list) == 0:
        caught_text1 = "You have not caught"
        caught_text2 = "any Pokemon"
        caught_msg = word_font.render(caught_text1, False, (100, 220, 250))
        win.blit(caught_msg, (winWidth / 2 - 150, 20))
        caught_msg = word_font.render(caught_text2, False, (100, 220, 250))
        win.blit(caught_msg, (winWidth / 2 - 100, 50))
    else:
        caught_msg1 = word_font.render(caught_text1, False, (100, 220, 250))
        win.blit(caught_msg1, (winWidth / 2 - 130, 20))
        caught_msg2 = word_font.render(caught_text2, False, (100, 220, 250))
        win.blit(caught_msg2, (winWidth / 2 - 105, 55))

    for poke in range(len(caught_list)):
        poke_text = str(poke + 1) + ". " + caught_list[poke]
        poke_msg = caught_font.render(poke_text, False, Color["white"])
        win.blit(poke_msg, (winWidth / 2 - 130, 100 + poke * 30))


# Decides the difficulty of the current pokemon based on its cp.
def decide_difficulty():
    cp = pokemon.get_cp()
    if cp < 200:
        difficulty = 1
    elif cp < 400:
        difficulty = 2
    elif cp < 600:
        difficulty = 3
    elif cp < 800:
        difficulty = 4
    else:
        difficulty = 5
    return difficulty


# Creates a new pokemon.
def change_pokemon():
    global poke_changed

    # Creates a new pokemon.
    pokemon.randomize_pokemon()

    # Randomizes the cp and decides the difficulty.
    pokemon.set_cp(random.randint(1, 1000))
    difficulty = decide_difficulty()

    # Gets the position of the pokemon and puts the circle at their position.
    x, y = pokemon.get_pos()
    x += pokemon.get_radius()
    y += pokemon.get_radius()
    catch_circle.set_pos(x, y)

    # Randomly sets the size of the catching circle for the new pokemon and the colour.
    catch_circle.set_radius(random.randint(1, 5))
    catch_circle.reset_radius()
    catch_circle.set_colour(difficulty)
    catch_circle.set_speed(random.randint(1, 3))

    poke_changed = True


# Display coordinates of pokemon and catch radius for testing.
def display_test():
    poke_x, poke_y = pokemon.get_pos()
    poke_x, poke_y = round(poke_x, 2), round(poke_y, 2)
    poke_name = pokemon.get_name()
    poke_radius = round(pokemon.get_radius(), 2)
    poke_text = (
        poke_name
        + " x, y: "
        + str(poke_x)
        + ", "
        + str(poke_y)
        + ", radius = "
        + str(poke_radius)
    )
    poke_msg = caught_font.render(poke_text, False, (250, 250, 250))
    win.blit(poke_msg, (10, 20))

    radius_x, radius_y = round(catch_circle.get_x_pos(), 2), round(
        catch_circle.get_y_pos(), 2
    )
    radius_radius = round(catch_circle.get_radius(), 2)
    radius_text = (
        "Radius x, y: "
        + str(radius_x)
        + ", "
        + str(radius_y)
        + ", radius = "
        + str(radius_radius)
    )
    radius_msg = caught_font.render(radius_text, False, (250, 250, 250))
    win.blit(radius_msg, (10, 50))


menu.main_menu()
pygame.display.set_caption("Mon-Poke")

# Makes it so that eevee isn't the automatic first pokemon.
change_pokemon()

while True:

    keysPressed = pygame.key.get_pressed()

    # If the user quits the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Stuff the user can do if the pokemon hasn't been caught yet.
    if not poke_caught:
        # When the user makes the thrower bigger or smaller.
        if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]:
            throw_line.change_length(1)
        elif keysPressed[pygame.K_s] or keysPressed[pygame.K_DOWN]:
            throw_line.change_length(-1)

        # When the user makes the thrower go left or right.
        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
            throw_line.change_angle(-1)
        elif keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
            throw_line.change_angle(1)

        # When the user presses space to jump. If statement ensures they cannot jump while already jumping.
        if keysPressed[pygame.K_SPACE]:

            # Checks if the line was visible before pressing space.
            line_visible = False
            if throw_line.get_visibility():
                line_visible = True

            # Checks if the catch circle was visible before pressing space.
            circle_visible = False
            if catch_circle.get_visibility():
                circle_visible = True

            # Makes aiming line and circle invisible.
            throw_line.change_visible(False)
            catch_circle.set_visibility(False)

            if not hasPressed:
                hasPressed = True
                for i in range(7):
                    ball.y -= 10

                    win.blit(win_background, (0, 0))
                    ball.draw_ball(win, Color, poke_caught and not ball_caught)
                    pygame.display.flip()
                    pygame.time.delay(30)
                for i in range(7):
                    ball.y += 10

                    win.blit(win_background, (0, 0))
                    ball.draw_ball(win, Color, poke_caught and not ball_caught)
                    pygame.display.flip()
                    pygame.time.delay(30)

                # Makes the line visible again if it was originally.
                if line_visible:
                    # Makes aiming line visible.
                    throw_line.change_visible(True)
                # Makes the circle visible again if it was originally.
                if circle_visible:
                    # Makes circle visible.
                    catch_circle.set_visibility(True)
            else:
                hasPressed = False

                # Makes the ball visible again if it was originally.
                if line_visible:
                    # Makes aiming line visible.
                    throw_line.change_visible(True)
                # Makes the circle visible again if it was originally.
                if circle_visible:
                    # Makes circle visible.
                    catch_circle.set_visibility(True)

        # The user presses a key to throw the ball
        elif keysPressed[pygame.K_x]:
            if not ballMoved:
                angle = throw_line.get_angle() * math.pi / 180
                speed = throw_line.get_length() / 4
                ball.throw_ball(
                    win,
                    Color,
                    clock,
                    speed,
                    win_background,
                    angle,
                    pokemon,
                    poke_caught and not ball_caught,
                    catch_circle,
                )
                ballMoved = True

                # Makes aiming line invisible.
                throw_line.change_visible(False)

                # Checks if the user caught the pokemon.
                if pokemon.pokemon_caught(ball.get_x_pos(), ball.get_y_pos()):
                    poke_caught = True
                    caught_poke()
                # Has the ball bounce past the pokemon if it was not caught.
                else:
                    # Calls this method a twice so it bounces twice.
                    ball.bounce_past(
                        win,
                        Color,
                        win_background,
                        pokemon,
                        clock,
                        poke_caught and not ball_caught,
                        catch_circle,
                    )
                    # Checks if the user caught the pokemon.
                    if pokemon.pokemon_caught(ball.get_x_pos(), ball.get_y_pos()):
                        poke_caught = True
                    if poke_caught:
                        caught_poke()
                    else:
                        ball.bounce_past(
                            win,
                            Color,
                            win_background,
                            pokemon,
                            clock,
                            poke_caught and not ball_caught,
                            catch_circle,
                        )
                        # Checks if the user caught the pokemon.
                        if pokemon.pokemon_caught(ball.get_x_pos(), ball.get_y_pos()):
                            poke_caught = True
                            caught_poke()

        # Resets the ball to its original position to give the user another shot.
        elif keysPressed[pygame.K_z]:
            ball.set_pos(ball_start_x, ball_start_y)
            ball.change_radius(ball_radius1)
            ballMoved = False

            # Makes aiming line visible and resets it.
            throw_line.change_visible(True)
            throw_line.reset_throw()
            display_poke = False

    # Resets the ball to its original position and changes the pokemon.
    if keysPressed[pygame.K_c]:
        ball.set_pos(ball_start_x, ball_start_y)
        ball.change_radius(ball_radius1)
        ballMoved = False

        # Only changes the pokemon if it wasn't just changed.
        if not poke_changed:
            change_pokemon()

        # Makes aiming line visible.
        throw_line.change_visible(True)
        throw_line.reset_throw()
        poke_caught = False
        ball_caught = False
        failed_catch = False
        display_poke = False
        num_tries = 0
        pokemon.set_visibility(True)

    # Shows what pokemon have been caught.
    if keysPressed[pygame.K_p] or display_poke:
        display_poke = True
        display_caught()

    # If it is showing which pokemon have been caught, goes back to normal screen.
    if keysPressed[pygame.K_z] and display_poke:
        display_poke = False

    if not display_poke:

        win.blit(win_background, (0, 0))

        pokemon.draw_self(win)

        ball.draw_ball(win, Color, poke_caught and not ball_caught)
        throw_line.draw_throw(win)

        # Draws a message showing that the pokemon was caught if it was.
        if ball_caught and poke_caught:
            draw_caught_msg()
        # If the pokemon was not caught, shows the circle.
        elif not poke_caught:
            catch_circle.draw_circle(win)

        # Has the pokemon jump.
        if not poke_caught and not ball_caught:
            # Increments the timer for the pokemon jumping and sees if it reached the max.
            poke_timer += 1
            if poke_timer == poke_timer_max:
                poke_timer_max = random.randint(100, 500)
                poke_timer = 0
                pokemon.jump(
                    win,
                    win_background,
                    throw_line,
                    ball,
                    Color,
                    poke_caught and not ball_caught,
                )

            # Ensures that the pokemon can't be infinitely changed.
            if poke_changed:
                poke_change_timer += 1
                if poke_change_timer == 35:
                    poke_change_timer = 0
                    poke_changed = False

    # Goes back to the main menu.
    if keysPressed[pygame.K_TAB]:

        # Changes window size to menu size.
        win = pygame.display.set_mode((380, 350), 0, 32)
        menu.main_menu()

        # Brings window back to normal size
        win = pygame.display.set_mode((winWidth, winHeight))

        # Randomizes background for now.
        background_choice = f'backgrounds/pokemon_background{random.randint(1, 6)}.png'
        win_background = pygame.image.load(background_choice)
        pygame.display.set_caption("Mon-Poke")

    # Test method for seeing where the pokemon is compared to the radius.
    # display_test()

    pygame.display.flip()
    clock.tick(60)
