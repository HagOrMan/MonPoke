import pygame
import random
import math


# Makes a list of all the png file names for all pokemon.
def make_poke_list():
    poke_list = []

    f = open("pokemons.txt", "rt")

    listpokemon = []
    for line in f:
        listthingies = line.split()
        listpokemon.append(listthingies[1])

    f.close()

    pokemon = listpokemon
    distances = ["close", "medium", "far"]

    # Makes a list of all the pokemon and all their distances as the name of their png files.
    for poke in pokemon:
        for dist in distances:
            poke_list.append(poke + "_" + dist + ".png")
    print(poke_list)
    return poke_list


# Decides the name of the pokemon.
def decide_name(image: str):
    name = image.split("_")[0]
    name = name.capitalize()
    return name

# prof1p10_close


class Pokemon:
    def __init__(
        self, winWidth: int, winHeight: int, poke_type: str, image="eevee_close.png"
    ):
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.radius = 0
        self.x, self.y = self.decide_start(image)
        self.shadow_x, self.shadow_y = self.x, self.y
        self.image = pygame.image.load(image)
        self.shadow = pygame.image.load("backgrounds/shadow_close.png")
        self.poke_list = make_poke_list()
        self.visible = True
        self.name = decide_name(image)
        self.type = poke_type
        self.CP = 0
        self.stats = [0, 0, 0]  # [attack, defense, stamina] - max 15
        self.IV = 0

    # Decides the starting position of the pokemon based on whether it is close, medium, or far.
    def decide_start(self, image: str):
        position = image.split("_")[1]

        # Randomizes where the pokemon is on the field so it's not always centered.
        rand_x, rand_y = random.random(), random.random()

        if position == "close.png":

            # Sets self parameter of the "radius" of catching.
            self.radius = 65

            if self.winWidth * rand_x + self.radius * 2 > self.winWidth:
                x = self.winWidth * rand_x - self.radius * 2
            else:
                x = self.winWidth * rand_x

            self.shadow = pygame.image.load("backgrounds/shadow_close.png")
        elif position == "medium.png":

            self.radius = 55

            if self.winWidth * rand_x + self.radius * 2 > self.winWidth:
                x = self.winWidth * rand_x - self.radius * 2
            else:
                x = self.winWidth * rand_x

            self.shadow = pygame.image.load("backgrounds/shadow_medium.png")
        else:

            self.radius = 40

            if self.winWidth * rand_x + self.radius * 2 > self.winWidth:
                x = self.winWidth * rand_x - self.radius * 2
            else:
                x = self.winWidth * rand_x

            self.shadow = pygame.image.load("backgrounds/shadow_far.png")

        if rand_y > 0.4:
            y = self.winHeight * 0.4
        else:
            y = self.winHeight * rand_y

        return x, y

    # Draws the pokemon at its position
    def draw_self(self, win):
        if self.visible:
            win.blit(self.shadow, (self.shadow_x, self.shadow_y))
            win.blit(self.image, (self.x, self.y))

    # Randomly creates a new pokemon.
    def randomize_pokemon(self):
        rand = random.randint(0, len(self.poke_list) - 1)
        self.change_image(self.poke_list[rand])

    # Has the pokemon jump up and down.
    def jump(self, win, win_background, throw_line, ball, Color, poke_caught):
        jump_height = random.randint(3, 7)
        for i in range(jump_height):
            self.y -= 10
            # win.fill(winColor)
            win.blit(win_background, (0, 0))
            ball.draw_ball(win, Color, poke_caught)
            self.draw_self(win)
            throw_line.draw_throw(win)
            pygame.display.flip()
            pygame.time.delay(30)
        for i in range(jump_height):
            self.y += 10
            # win.fill(winColor)
            win.blit(win_background, (0, 0))
            ball.draw_ball(win, Color, poke_caught)
            self.draw_self(win)
            throw_line.draw_throw(win)
            pygame.display.flip()
            pygame.time.delay(30)

    # Checks if a point is close enough to the pokemon to catch it.
    def pokemon_caught(self, x: float, y: float):
        middle_x = self.x + self.radius
        middle_y = self.y + self.radius

        distance = math.sqrt((middle_x - x) ** 2 + (middle_y - y) ** 2)

        if distance <= self.radius * 1.25:
            return True
        else:
            return False

    # Getters
    def get_pos(self):
        return self.x, self.y

    def get_poke_list(self):
        return self.poke_list

    def get_radius(self):
        return self.radius

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_cp(self):
        return self.CP

    def get_stats(self):
        return self.stats

    def get_iv(self):
        return self.IV

    # Setters
    def set_pos(self, x: float, y: float):
        self.x, self.y = x, y


    def set_visibility(self, visible: bool):
        self.visible = visible

    def set_cp(self, value: float):
        self.CP = value
        return self.CP

    def power_up(self, value: float):
        self.CP += value
        return self.CP

    def set_stats(self, attack: float, defense: float, stamina: float):
        if attack > 15 or defense > 15 or stamina > 15:
            print("Sorry, values cannot exceed 15.")
        else:
            self.stats = [attack, defense, stamina]
            self.IV = sum(self.stats) / 45 * 100
        return self.IV

    def display_details(self):
        print("Name:\t", self.get_name())
        print("Type:\t", self.get_type())
        print("CP:\t", self.get_cp())
        stats = self.get_stats()
        print("Attack:\t", stats[0])
        print("Defense:", stats[1])
        print("Stamina:", stats[2])
        print("IV:\t", self.get_iv)

    # Changes the image of the pokemon.
    def change_image(self, image):
        try:
            self.image = pygame.image.load("pokemon_pics/"+image)

            # Since there is a new image, changes what its position is.
            self.set_pos(self.decide_start(image)[0], self.decide_start(image)[1])

            # Gives the shadow its own coordinates that won't change as the pokemon moves.
            self.shadow_x, self.shadow_y = self.x, self.y + self.radius + 10

            # Changes the name to the new name.
            self.name = decide_name(image)

        except FileNotFoundError:
            self.randomize_pokemon()
