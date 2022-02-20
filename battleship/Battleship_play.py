# Author Callum MacKinnon

# TODO: BOT ships can wrap on the sides (check all) happened on N.
# TODO: Add a Finish screen
# TODO: Change some of the output colours - Magenta for player hit etc
# TODO: Make BOT more human. ie if hit localise hits.
# TODO: Add a live debuggers file. Adds grids on every move to file.

# TODO: ADD another column to display. For Ship updates -- BOT ships, Player Ships to show what
#  is dead and what is alive. Maybe make gap from 3 to 2 between ship and hit grid to make space.
#  np.array along the bottom maybe under the gtrids.

import os
import random
import platform
import numpy as np
from termcolor import colored, cprint
import time

if platform.system() == 'Windows':
    _EXT = 'cls'
elif platform.system() == 'macOS':
    _EXT = 'clear'
elif platform.system() == 'Darwin':
    _EXT = 'clear'
os.system(_EXT)


# TODO: Add the postion selection for the bot. Maybe add a differnet class?
class ConsoleOutput:
    @staticmethod
    def output_error(error):
        error_diction = {
            0: '-- Invalid Position: Chose a valid input -- ',
            1: '-- Ship Overlapping: Chose a valid placement --',
            2: '-- Invalid Input: 0 <= Input <= 99 --',
            3: '-- Invalid Input: Heading not in N, E, S, W --',
            4: '-- Invalid Position: Ship is hanging off the north side of the board --',
            5: '-- Invalid Position: Ship is hanging off the south side of the board --',
            6: '-- Invalid Position: Ship is hanging off the east side of the board --',
            7: '-- Invalid Position: Ship is hanging off the west side of the board --',
            8: '-- Invalid Hit: Position has already been hit --',
            9: '-- Invalid Hit: Position not in grid --',
            }
        return print(colored(error_diction[error], 'red'))

    @staticmethod
    def output_message(id_take, arg=''):
        error_diction = {
            0: '-- Enter number of square to start and then North(N), South(S), East (E) or West('
               'W) from starting position -- Example: 44 then N',
            1: f'-- HIT at {arg}! --',
            }
        return error_diction[id_take]

    @staticmethod
    def game_message(id_take, arg=''):
        error_diction = {
            'SUNK OP': f'ENEMY: SUNK your {arg}!',
            'HIT OP': f'ENEMY: HIT your {arg}!',
            'MISS OP': 'ENEMY: MISSED!',

            'SUNK PL': f'{Game.player.name}: SUNK the enemy\'s {arg}!',
            'HIT PL': f'{Game.player.name}: HIT at {arg}!',
            'MISS PL': f'{Game.player.name}: MISS at {arg}!',
            }
        return error_diction[id_take]


class PlayerSetUp(object):

    def __init__(self, name):
        """ Adds all information to the player object. Name grid and all ships"""
        self.name = name
        self.HP = 17
        self.guesses = []
        # The players gird
        self.hit_grid = np.array([[f'{j}{i}' for i in list(range(10))] for j in list('ABCDEFGHIJ')])

        self.ship_grid = np.array([[f'{j}{i}' for i in list(range(10))] for j in
                                   list('ABCDEFGHIJ')])

        # All possible ships to be stored in the player object: passing name, shorthand and length
        self.carrier = ShipInfo('Carrier', 'Ca', 5, 'green')
        self.battleship = ShipInfo('Battleship', 'Bt', 4, 'yellow')
        self.cruiser = ShipInfo('Cruiser', 'Cr', 3, 'blue')
        self.submarine = ShipInfo('Submarine', 'Sb', 3, 'magenta')
        self.destroyer = ShipInfo('Destroyer', 'Dy', 2, 'cyan')

        self.fleet = [self.carrier, self.battleship, self.cruiser, self.submarine, self.destroyer]
        Testing = False
        if Testing:
            PreAllocate(self.fleet, self.ship_grid, self.name)
        else:
            # Place the ships now they are object inside the player
            PlaceFleetPlayer(self.fleet, self.ship_grid)

        self.hit_pos = {ship: ship.position for ship in self.fleet}

    @staticmethod
    def show_grid(grid_ships, grid_hit):
        filler = np.array([['  ' for i in range(1)] for j in range(10)])
        filler2 = np.array([['#' for i in range(1)] for j in range(10)])

        new = np.hstack((grid_ships, filler, filler2, filler, grid_hit))

        col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*new))}

        # print using the column index from enumerate to lookup this columns lenght
        print(colored(f"{15 * ' '}{'--- Ship Grid ---'}{50 * ' '}{'---Hit Grid---'}", 'green'))
        for inner in new:
            # print(len(inner))
            for col, word in enumerate(inner):
                if word in ['Ca', 'Cr', 'Bt', 'Sb', 'Dy']:
                    word = colored(word, 'magenta')
                else:
                    word = colored(word, 'cyan')

                print(f"{colored(word, 'cyan'):{col_len[col]}}", end=" | ")
            print()


class BotSetUp(object):

    def __init__(self, name):
        """ Adds all information to the player object. Name grid and all ships"""
        self.name = name
        self.HP = 17
        self.guesses = []
        # The players gird
        self.hit_grid = np.array([[j + str(i) for i in list(range(10))] for j in
                                  list('ABCDEFGHIJ')])

        self.ship_grid = np.array([[j + str(i) for i in list(range(10))] for j in
                                   list('ABCDEFGHIJ')])

        # All possible ships to be stored in the player object: passing name, shorthand and length
        self.carrier = ShipInfo('Carrier', 'Ca', 5, 'green')
        self.battleship = ShipInfo('Battleship', 'Bt', 4, 'yellow')
        self.cruiser = ShipInfo('Cruiser', 'Cr', 3, 'blue')
        self.submarine = ShipInfo('Submarine', 'Sb', 3, 'magenta')
        self.destroyer = ShipInfo('Destroyer', 'Dy', 2, 'cyan')

        self.fleet = [self.carrier, self.battleship, self.cruiser, self.submarine, self.destroyer]
        Testing = False
        if Testing:
            PreAllocate(self.fleet, self.ship_grid, self.name)
        else:
            # Place the ships now they are object inside the player
            PlaceFleetBot(self.fleet, self.ship_grid)

        self.hit_pos = {ship: ship.position for ship in self.fleet}

    @staticmethod
    def show_grid(grid_ships, grid_hit):
        filler = np.array([['  ' for i in range(1)] for j in range(10)])
        filler2 = np.array([['#' for i in range(1)] for j in range(10)])

        new = np.hstack((grid_ships, filler, filler2, filler, grid_hit))

        col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*new))}

        # print using the column index from enumerate to lookup this columns lenght
        print(colored(f"{15 * ' '}{'--- Ship Grid ---'}{50 * ' '}{'---Hit Grid---'}", 'green'))
        for inner in new:
            # print(len(inner))
            for col, word in enumerate(inner):
                if word in ['Ca', 'Cr', 'Bt', 'Sb', 'Dy']:
                    word = colored(word, 'magenta')
                else:
                    word = colored(word, 'cyan')

                print(f"{colored(word, 'cyan'):{col_len[col]}}", end=" | ")
            print()


class PreAllocate(object):
    """Places player's ships into onto their grid and makes sure they are valid"""

    def __init__(self, fleet, grid, name):
        self.live_grid = grid
        if name == 'BOT':
            fleet[0].position, fleet[0].initialise, fleet[0].heading = [
                ['G5', 'F5', 'E5', 'D5', 'C5'], 'G5', 'N']

            fleet[1].position, fleet[1].initialise, fleet[1].heading = [['E4', 'E3', 'E2', 'E1'],
                                                                        'E4', 'W']
            fleet[2].position, fleet[2].initialise, fleet[2].heading = [['H8', 'G8', 'F8'], 'H8',
                                                                        'N']
            fleet[3].position, fleet[3].initialise, fleet[3].heading = [['I1', 'H1', 'G1'], 'I1',
                                                                        'N']
            fleet[4].position, fleet[4].initialise, fleet[4].heading = [['J4', 'J5'], 'J4', 'E']
        else:
            fleet[0].position, fleet[0].initialise, fleet[0].heading = [
                ['A0', 'A1', 'A2', 'A3', 'A4'], 'A0', 'E']

            fleet[1].position, fleet[1].initialise, fleet[1].heading = [['E4', 'F4', 'G4', 'H4'],
                                                                        'E4', 'S']
            fleet[2].position, fleet[2].initialise, fleet[2].heading = [['F6', 'G6', 'H6'], 'F6',
                                                                        'S']
            fleet[3].position, fleet[3].initialise, fleet[3].heading = [['I3', 'I4', 'I5'], 'I3',
                                                                        'E']
            fleet[4].position, fleet[4].initialise, fleet[4].heading = [['I8', 'I7'], 'I8', 'W']
        for ship in fleet:
            for idx, location in enumerate(ship.position):
                i = np.where(self.live_grid == location)
                self.live_grid[i[0][0]][i[1][0]] = ship.shorthand


class PlaceFleetPlayer(object):
    """Places player's ships into onto their grid and makes sure they are valid"""

    def __init__(self, fleet, grid):
        self.live_grid = grid
        grid_taken = []  # A dynamic list containing the taken position in terms of integer numbers
        ConsoleOutput.output_message(0)
        self.show_grid(self.live_grid)

        for ship in fleet:  # Take each ship object
            ship.position = None
            while ship.position is None:  # any error will send out None
                ship.initialise = input(f'Enter starting position of {ship.shipname}: ').upper()  #
                ship.heading = input('Enter direction:  ').upper()  # string N,E,S,W
                if self.input_valid(ship.initialise, ship.heading, self.live_grid) is not None:

                    # Take the ship position and heading and determine the array location
                    # Also check to see if the location is valid
                    ship.position = self.determine_coord(ship.initialise,
                                                         ship.heading,
                                                         ship.length,
                                                         grid_taken)

            for spot in ship.position:
                grid_taken.append(spot)

            for idx, location in enumerate(ship.position):
                i = np.where(self.live_grid == location)
                self.live_grid[i[0][0]][i[1][0]] = ship.shorthand

            self.show_grid(self.live_grid)

    @staticmethod
    def input_valid(start, heading, grid):
        if start not in grid:
            ConsoleOutput.output_error(2)
            return None
        elif heading not in list('NESW'):
            ConsoleOutput.output_error(3)
            return None
        else:
            return ''

    def determine_coord(self, start, heading, ship_length, taken_spots):
        """Determines the coordinated of the player's input"""

        letters = list('ABCDEFGHIJ')
        numbers = list(range(10))
        index = letters.index(start[0])
        # Creating a wrap around effect to generate coordinates to check
        if heading in list('EW'):
            if heading == 'W':
                numbers = numbers[::-1]
            while str(numbers[0]) != start[1]:
                numbers.append(numbers.pop(0))
            grid_number = [f'{start[0]}{numbers[ind]}' for ind in range(ship_length)]
        else:
            if heading == 'N':
                letters = letters[::-1]
            while letters[0] != start[0]:
                letters.append(letters.pop(0))

            grid_number = [f'{letters[ind]}{start[1]}' for ind in range(ship_length)]

        if not self.check_coord(grid_number, heading, taken_spots):
            return None
        else:
            positional_coords = [ship for ship in grid_number]
            return positional_coords

    def check_coord(self, coordinates, heading, taken_spots):
        """ Check if input in in the bounds of the board or if it overlaps another ship"""

        for spots in coordinates:
            if spots in taken_spots:
                ConsoleOutput.output_error(1)
                return False

        if heading in list("EW"):
            if heading == 'E':
                if coordinates[0][1] > coordinates[-1][1]:
                    ConsoleOutput.output_error(6)
                    return False
            else:
                if coordinates[0][1] < coordinates[-1][1]:
                    ConsoleOutput.output_error(7)
                    return False

        else:  # else if NW
            for location in coordinates:
                if location not in np.array([[j + str(i) for i in list(range(10))] for j in
                                             list('ABCDEFGHIJ')]):
                    ConsoleOutput.output_error(0)
                    return False
            else:

                for idx in range(1, len(coordinates)):
                    # print(coordinates[idx - 1], coordinates[idx])
                    if (coordinates[idx - 1][0] == 'A') and (coordinates[idx][0] == 'J'):
                        ConsoleOutput.output_error(4)
                        return False
                    if (coordinates[idx - 1][0] == 'J') and (coordinates[idx][0] == 'A'):
                        ConsoleOutput.output_error(5)
                        return False
                return True
            return True
        return True

    @staticmethod
    def show_grid(grid):
        # transpose the list, get the max of each column and store in as dict[column]=legnth
        col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*grid))}

        # print using the column index from enumerate to lookup this columns lenght
        for inner in grid:
            for col, word in enumerate(inner):
                if word in ['Ca', 'Cr', 'Bt', 'Sb', 'Dy']:
                    word = colored(word, 'magenta')
                else:
                    word = colored(word, 'cyan')

                print(f"{colored(word, 'cyan'):{col_len[col]}}", end=" | ")
            print()


class PlaceFleetBot(object):
    """Places player's ships into onto their grid and makes sure they are valid"""

    def __init__(self, fleet, grid):
        self.live_grid = grid
        grid_taken = []
        choices = [j for i in Game.grid for j in i]

        for ship in fleet:  # Take each ship object
            ship.position = None
            while ship.position is None:  # any error will send out None
                ship.initialise = choices[random.randint(0, len(choices) - 1)]
                ship.heading = list('NESW')[random.randint(0, 3)]

                ship.position = self.determine_coord(ship.initialise,
                                                     ship.heading,
                                                     ship.length,
                                                     grid_taken)

            print(f'Ship position is {ship.position}')
            for spot in ship.position:
                grid_taken.append(spot)
                choices.remove(spot)

    def determine_coord(self, start, heading, ship_length, taken_spots):

        letters = list('ABCDEFGHIJ')
        numbers = list(range(10))
        index = letters.index(start[0])
        # Creating a wrap around effect to generate coordinates to check
        if heading in list('EW'):
            if heading == 'W':
                numbers = numbers[::-1]
            while str(numbers[0]) != start[1]:
                numbers.append(numbers.pop(0))
            grid_number = [f'{start[0]}{numbers[ind]}' for ind in range(ship_length)]
        else:
            if heading == 'N':
                letters = letters[::-1]
            while letters[0] != start[0]:
                letters.append(letters.pop(0))

            grid_number = [f'{letters[ind]}{start[1]}' for ind in range(ship_length)]

        if not self.check_coord(grid_number, heading, taken_spots):
            return None
        else:
            positional_coords = [ship for ship in grid_number]
            return positional_coords

    def check_coord(self, coordinates, heading, taken_spots):
        """ Check if input in in the bounds of the board or if it overlaps another ship"""

        for spots in coordinates:
            if spots in taken_spots:
                return False

        if heading in list("EW"):
            if heading == 'E':
                if coordinates[0][1] > coordinates[-1][1]:
                    return False
            else:
                if coordinates[0][1] < coordinates[-1][1]:

                    return False

        else:  # else if NW

            for idx in range(1, len(coordinates)):
                if (coordinates[idx - 1][0] == 'A') and (coordinates[idx][0] == 'J'):
                    print('crossing')

                    return False
                if (coordinates[idx - 1][0] == 'J') and (coordinates[idx][0] == 'A'):
                    print('crossing')

                    return False
                return True
            return True
        return True


class ShipInfo(object):
    def __init__(self, name, shorthand, length, colour):
        self.shipname = name
        self.shorthand = shorthand
        self.length = length
        self.hp = length
        self.colour = colour


class Game(object):
    """ CLASS for defining the game. Every object if help within Class then within player.
    Player contained everything"""

    def __init__(self):
        self.player = ''
        self.bot = ''
        self.grid = np.array([[f'{j}{i}' for i in list(range(10))] for j in list('ABCDEFGHIJ')])

    def initialise(self):
        """Initialises the game by sending players to place ships in their GameInfo
        @return: None """
        self.player = PlayerSetUp('Player 1')
        self.bot = BotSetUp('BOT')
        # print('player grid',self.player.ship_grid)  # print(
        # '\n\n\n\nbot grid', self.bot.ship_grid)

        Game_on = PlayGame(self.player, self.bot)


class PlayGame(object):
    def __init__(self, p1, bot):
        # print(Game.grid)
        self.player = p1
        self.BOT = bot
        self.BOT.guesses = [j for i in Game.grid for j in i]

        self.game_message_buffer = [['Game Output(s)', 'white']]

        self.show_grid()
        self.round()

    def round(self):
        while (self.player.HP != 0) and (self.BOT.HP != 0):
            valid = False
            while not valid:
                player_guess = input('Select your hit: ').upper()
                valid = self.check_hit(player_guess)

            os.system(_EXT)
            self.update_grids(self.player_hit_op(player_guess), player_guess)
            self.show_grid()
            time.sleep(1)
            self.bot_backend()
            time.sleep(1)
            os.system(_EXT)
            self.show_grid()

    def check_hit(self, guess):
        # error if guess has already happened
        if guess in self.player.guesses:
            ConsoleOutput.output_error(8)
            return False
        # error if guess is not in the grid
        elif guess not in self.player.hit_grid:
            ConsoleOutput.output_error(9)
            return False
        else:
            return True

    def player_hit_op(self, guess):
        self.player.guesses.append(guess)

        # Check if a ship has been hit
        for ship in self.BOT.hit_pos:
            for coords in self.BOT.hit_pos[ship]:
                if guess in coords:
                    self.message_buffer(ConsoleOutput.game_message('HIT PL', guess), 'green')
                    self.BOT.HP -= 1
                    ship.hp -= 1
                    if ship.hp == 0:
                        self.message_buffer(ConsoleOutput.game_message('SUNK PL', ship.shipname),
                                            'magenta')
                    return True
        else:
            self.message_buffer(ConsoleOutput.game_message('MISS PL', guess), 'green')
            return False

    def update_grids(self, hit_boo, guess):
        # update the hit gris first
        if hit_boo:
            self.player.hit_grid = np.where(self.player.hit_grid == guess,
                                            'XX',
                                            self.player.hit_grid)
        else:
            self.player.hit_grid = np.where(self.player.hit_grid == guess,
                                            '[]',
                                            self.player.hit_grid)

    def show_grid(self):

        filler = np.array([['  ' for i in range(1)] for j in range(10)])
        filler2 = np.array([['#' for i in range(1)] for j in range(10)])

        new = np.hstack((self.player.ship_grid, filler, filler2, filler, self.player.hit_grid))

        col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*new))}

        # print using the column index from enumerate to lookup this columns lenght
        print(colored(f"{15 * ' '}{'--- Ship Grid ---'}{49 * ' '}{'---Hit Grid---'}", 'green'))
        for MSG, inner in enumerate(new):
            # print(len(inner))
            for col, word in enumerate(inner):
                if word in ['Ca', 'Cr', 'Bt', 'Sb', 'Dy']:
                    word = colored(word, 'magenta')
                elif word == 'XX':
                    word = colored(word, 'red')
                elif word == '[]':
                    word = colored(word, 'yellow')

                print(f"{colored(word, 'cyan'):{col_len[col]}}", end=" | ")
            try:
                if MSG == 0:
                    print('\t\t|' + colored(f'{self.game_message_buffer[MSG][0]}', 'white'))
                elif MSG in list(range(1, 4)):
                    print('\t\t|' + colored(f'{self.game_message_buffer[MSG][0]}',
                                            self.game_message_buffer[MSG][1]))
                else:
                    print('\t\t|' + colored(f'{self.game_message_buffer[MSG][0]}', 'grey'))
            except IndexError:
                print(f'\t\t|')

    def bot_backend(self):
        # make a selection at random
        bot_choice = self.BOT.guesses[random.randint(0, len(self.BOT.guesses) - 1)]

        self.BOT.guesses.remove(bot_choice)

        for ship in self.player.hit_pos:
            if bot_choice in self.player.hit_pos[ship]:

                self.player.ship_grid = np.where(Game.grid == bot_choice,
                                                 'XX',
                                                 self.player.ship_grid)
                self.player.HP -= 1
                ship.hp -= 1

                if ship.hp == 0:
                    self.message_buffer(ConsoleOutput.game_message('SUNK OP', ship.shipname), 'red')
                else:
                    self.message_buffer(ConsoleOutput.game_message('HIT OP', ship.shipname),
                                        'yellow')
                break
        else:
            self.player.ship_grid = np.where(self.player.hit_grid == bot_choice,
                                             '[]',
                                             self.player.ship_grid)
            self.message_buffer(ConsoleOutput.game_message('MISS OP'), 'yellow')

    def message_buffer(self, msg, color):

        if len(self.game_message_buffer) <= 10:
            self.game_message_buffer.insert(1, [msg, color])
        else:
            self.game_message_buffer.pop(-1)
            self.game_message_buffer.insert(1, [msg, color])


if __name__ == '__main__':

    Game = Game()

    Game.initialise()
