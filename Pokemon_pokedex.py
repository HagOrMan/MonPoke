import random, math
from datetime import datetime

# imports pokemon from the save file
def import_pokes():
    pokemons = {}
    f = open("save.txt", "rt")

    counter = 0

    for line in f:
        # takes line from file and splits it into the different variables
        name, species, typ, level, CP, stats, IV, date, difficulty = (line.strip("\n")).split("-")
        # creates new unique id for pokemon
        pokemon_id = f"poke_{counter}"
        # adds pokemon object to the dictionary
        pokemons[pokemon_id] = pokemons.get(
            pokemon_id, PokemonDex(name=pokemon_id, species=species, difficulty=difficulty)
        )

        pokemons[pokemon_id].set_from_old(
            name, species, typ, level, CP, stats, IV, date
        )
        counter += 1


    f.close()
    return pokemons, counter


# adds pokemon to text file after the session is complete"""
def export_pokes(pokemons):
    # opens ave file
    w = open("save.txt", "wt")
    for i in range(len(pokemons)):
        name, species, typ, level, CP, stats, IV, date, difficulty = pokemons[
            f"poke_{i}"
        ].return_details()

        if(type(stats) == str):
            stats_list = stats.split(' ')
        else:
            stats_list = stats
        w.write(f"{name}-{species}-{typ}-{level}-{round(float(CP),2)}-{f'{stats_list[0]} {stats_list[1]} {stats_list[2]}'}-{IV}-{date}-{difficulty}\n")

    w.close()


# export the pokemon dictionary
def export_dic():
    pokemons, counter = import_pokes()
    return pokemons


# gets the date and returns it
def get_date():
    current_datetime = datetime.now()
    current_date = (
        f"{current_datetime.month}/{current_datetime.day}/{current_datetime.year}"
    )
    return current_date


'''pokedex class
class to store the captured pokemons, essentially the pokedex

functions:
- init
- set_list, sets the dictionary of pokemons to the save file
- get_type_list, gets the list of types of each pokemon
- get_type, gets the type of a certain pokemon, when passed the species. relies on the get_type_list
- get_list_index, gets the pokemon object from the dictionary given an index
- get_list_lengthm gets the length of the pokedex dictionary -- the amount of pokemons caught
- get_list, gets the full dictinary of pokemon; keys are "poke_##", while the value is a pokemon object
- add_pokemon, adds a pokemon to the pokedex after being caught in pokemon_game'''
class Pokedex:
    # definition
    def __init__(self):
        self.pokemons_dic = {}
        self.length = 0
        self.dic_types = {}

    # sets self.pokemons_dic to what is in the save file
    def set_list(self, save_file_name):
        pokemons = {}
        f = open(save_file_name)

        counter = 0

        for line in f:
            # takes line from file and splits it into the different variables
            name, species, typ, level, CP, unform_stats, IV, date, difficulty = (line.strip("\n")).split("-")
            level = int(level)
            self.get_type_list()
            typ = self.get_type(species.title())
            CP = round(float(CP),2)
            stats = unform_stats.split(' ')
            stats[0] = int(stats[0])
            stats[1] = int(stats[1])
            stats[2] = int(stats[2])
            IV = float(IV)
            difficulty = int(difficulty)
            # creates new unique id for pokemon
            pokemon_id = f"poke_{counter}"
            # adds pokemon object to the dictionary
            pokemons[pokemon_id] = pokemons.get(
                pokemon_id, PokemonDex(name=pokemon_id, species=species, difficulty=difficulty)
            )

            pokemons[pokemon_id].set_from_old(
                name, species, typ, level, CP, stats, IV, date
            )
            counter += 1
        self.pokemons_dic = pokemons
        f.close()
    
    # gets the list of types for each pokemon to be used when identifying the type of each pokemon. needs pokemons_types.txt
    def get_type_list(self):
        f = open('pokemons_types.txt', 'rt')
        dic_type = {}
        for line in f:
            index, species, typ = line.split('~')
            dic_type[species] = typ.strip('\n')
        self.dic_types = dic_type
        f.close()
    
    # uses the dictionary of types from get_type_list and uses it to return the list of a pokemon
    def get_type(self, species):
        return self.dic_types[species.title()]

    # gets the pokemon object given an index
    def get_list_index(self, index):
        return self.pokemons_dic[f'poke_{index}']

    # gets the length of the list of caught pokemon
    def get_list_length(self):
        counter = -1
        for item in self.pokemons_dic:
            counter += 1
        self.length = counter
        return counter

    # gets the full dictioanry of keys and values (pokemondex objects)
    def get_list(self):
        return self.pokemons_dic

    # adds pokemon given a species
    def add_pokemon(self, species, difficulty):
        counter = self.get_list_length()+1
        name = f'poke_{counter}'
        typ = self.get_type(species)
        new_pokemon = PokemonDex(name, species, difficulty)
        new_pokemon.set_type(typ)
        self.pokemons_dic[name] = new_pokemon

    def release(self, name):
        dic_storage = self.pokemons_dic
        if(name[-2:].isnumeric()):
            name_slice = int(name[-2:])
            for i in range(name_slice, self.get_list_length()):
                dic_storage[f'poke_{i}'] = self.pokemons_dic[f'poke_{i+1}']
        else:
            name_slice = int(name[-1:])
            for i in range(name_slice, self.get_list_length()):
                dic_storage[f'poke_{i}'] = self.pokemons_dic[f'poke_{i+1}']
        del dic_storage[f'poke_{self.get_list_length()}']

        for i in range(len(dic_storage)):
            print(dic_storage[f'poke_{i}'].get_level(), end = ' ')
        
        export_pokes(dic_storage)
        self.pokemons_dic = export_pokes

        print()


        
        


"""modified pokemon class

changes:
- added species, name is now the id number of the pokemon
- level & stats are randomly determined upon initiation
- changed up CP calculations
- added function set_from_old, which just sets the new pokemon with old session data
- added time caught"""
class PokemonDex:
    # definition
    def __init__(self, name, species, difficulty):
        self.difficulty = difficulty  # from kyle
        self.name = name
        self.type = 'placeholder'
        self.species = species
        # self.get_type_from_txt()
        self.stats = [
            random.randint(difficulty * 2, 15),
            random.randint(difficulty * 2, 15),
            random.randint(difficulty * 2, 15),
        ]
        self.level = random.randint(difficulty * 5 - 4, 40)
        self.CP = (
            (self.stats[0] + self.difficulty)
            * (self.stats[1] + self.difficulty) ** 0.5
            * (self.stats[2] + self.difficulty)
            * math.log(self.level)
            / 5
        )
        ## [attack, defense, stamina] - max 15
        self.IV = self.set_stats(self.stats[0], self.stats[1], self.stats[2])
        self.date = get_date()

    # get the name of the pokemon
    def get_name(self):
        return self.name

    # get the type of the pokemon
    def get_type(self):
        return self.type

    # sets the type of the pokemon, is called by the pokedex
    def set_type(self, typ):
        self.type = typ

    # gets the CP of the pokemon
    def get_CP(self):
        return self.CP

    # gets the stats of the pokemon
    def get_stats(self):
        return self.stats

    # gets the IV of the pokemon
    def get_IV(self):
        return round(self.IV, 2)

    # gets the level of the pokemon
    def get_level(self):
        return self.level

    # gets the species of the pokemon
    def get_species(self):
        return self.species

    # gets the date caught of the pokemon
    def get_date(self):
        return self.date

    # sets the pokemon from old save files given their information
    def set_from_old(self, name, species, typ, level, CP, stats, IV, date):
        self.name = name
        self.species = species
        self.type = typ
        self.stats = stats
        self.CP = CP
        self.level = level
        self.IV = float(IV)
        self.date = date

    # prints out the details to the screen
    def display_details(self):
        print("Name:\t", self.get_name())
        print("Type:\t", self.get_type())
        print("Level:\t", self.get_level())
        print("CP:\t", self.get_CP())
        stats = self.get_stats()
        print("Attack:\t", stats[0])
        print("Defense:", stats[1])
        print("Stamina:", stats[2])
        print("IV:\t", self.get_IV())
        print(f"Caught", self.get_date())

    # returns the details to the screen
    def return_details(self):
        return (
            self.get_name(),
            self.get_species(),
            self.get_type(),
            self.get_level(),
            self.get_CP(),
            self.get_stats(),
            self.get_IV(),
            self.get_date(),
            self.difficulty
        )

    # powers up the pokemon  by raising the level, and then returning the CP
    def power_up(self):
        self.level += 1
        self.CP = (
            (self.stats[0] + self.difficulty)
            * (self.stats[1] + self.difficulty) ** 0.5
            * (self.stats[2] + self.difficulty)
            * math.log(self.level)
            / 5
        )
        return self.CP

    # sets the stats
    def set_stats(self, attack, defense, stamina):
        if attack > 15 or defense > 15 or stamina > 15:
            print("Sorry, values cannot exceed 15.")
        else:
            self.stats = [attack, defense, stamina]
            self.IV = sum(self.stats) / 45 * 100
        return self.IV

# main function that was created for testing
def main():    
    pokemon1 = Pokedex()
    pokemon1.set_list("save.txt")
    dic_Pokemon = pokemon1.get_list()

    for i in range(len(dic_Pokemon)):
        dic_Pokemon[f"poke_{i}"].return_details()
    export_pokes(pokemon1.get_list())
