import numpy as np
# test
from termcolor import colored

global Testing


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
            7: '-- Invalid Position: Ship is hanging off the west side of the board --'
            }
        return print(colored(error_diction[error], 'red'))

    @staticmethod
    def output_message(id_take):
        error_diction = {
            0: '-- Enter number of square to start and then North(N), South(S), East (E) or West('
               'W) from starting position -- Example: 44 then N'
            }
        return print(colored(error_diction[id_take], 'green'))


class GameInfo(object):
    def __init__(self, name):
        """ Adds all information to the player object. Name grid and all ships"""
        self.name = name
        # The players gird
        self.grid = np.array([[j + str(i) for i in list(range(10))] for j in list('ABCDEFGHIJ')])

        self.display_grid = np.array([[j + str(i) for i in list(range(10))] for j in
                                      list('ABCDEFGHIJ')])

        # All possible ships to be stored in the player object: passing name, shorthand and length
        self.carrier = ShipInfo('Carrier', 'Ca', 5, 'green')
        self.battleship = ShipInfo('Battleship', 'Bt', 4, 'yellow')
        self.cruiser = ShipInfo('Cruiser', 'Cr', 3, 'blue')
        self.submarine = ShipInfo('Submarine', 'Sb', 3, 'magenta')
        self.destroyer = ShipInfo('Destroyer', 'Dy', 2, 'cyan')

        fleet = [self.carrier, self.battleship, self.cruiser, self.submarine, self.destroyer]

        if Testing:
            PreAllocate(fleet, self.display_grid, self.name)
        else:
            # Place the ships now they are object inside the player
            PlaceFleet(fleet, self.display_grid)

        self.hit_pos = {ship.shorthand: ship.position for ship in fleet}

        GameInfo.show_grid(self.display_grid,self.grid)

    @staticmethod
    def show_grid(grid_ships, grid_hit):
        filler = np.array([['  ' for i in range(1)] for j in range(10)])
        filler2 =  np.array([['#' for i in range(1)] for j in range(10)])

        new = np.hstack((grid_ships, filler,filler2,filler,grid_hit))

        col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*new))}

        # print using the column index from enumerate to lookup this columns lenght
        print(colored(f"{15 * ' '}{'--- Ship Grid ---'}{50 * ' '}{'---Hit Grid---'}", 'green'))
        for inner in new:
            # print(len(inner))
            for col, word in enumerate(inner):
                if word in ['Ca','Cr','Bt','Sb','Dy']:
                    word = colored(word,'magenta')
                else:word = colored(word,'cyan')



                print(f"{colored(word,'cyan'):{col_len[col]}}", end = " | ")
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


class PlaceFleet(object):
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
                print(f"{word:{col_len[col]}}", end=" | ")
            print()


class PlayGame(object):
    def __init__(self):
        # TODO: Play game here with hits etc

        print('IMPLEMENT')


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

    def initialise(self):
        """Initialises the game by sending players to place ships in their GameInfo
        @return: None """
        self.player = GameInfo('Player 1')
        # self.bot = GameInfo('BOT')
        # self.play_game(self.player, self.bot)

    def play_game(self, p1, bot):
        print('implement')


if __name__ == '__main__':
    Testing = True
    Game = Game()

    Game.initialise()

