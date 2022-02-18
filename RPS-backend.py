import random


class Players(object):
    """docstring for Players. Here you will ask for an input"""

    def __init__(self, name, score=0):

        self.name = name
        self.score = score

        if self.name == 'BOT FRED':
            self.input = ['ROCK', 'PAPER', 'SCISSORS'][random.randint(0, 2)]
        else:
            good_input = False
            while not good_input:
                self.input = input('%s: Rock(r), Papers(p) or Scissors(s)? ' % self.name).upper()
                if self.input in ['ROCK', 'PAPER', 'SCISSORS']:
                    good_input = True


class Round(object):
    """docstring for Round.Here you will ask each PLAYER to choose then compare and then award
    points """

    def __init__(self, p1, p2):
        locators = {
            'ROCK': 0,
            'PAPER': 1,
            'SCISSORS': 2
            }
        combinations = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
        result = combinations[locators[p1.input]][locators[p2.input]]

        Game.determine_winner(result)


class Game(object):
    """docstring for Game. here you will need ending coinidtions and winner dispaled"""

    def __init__(self):
        self.game_count = 0
        self.winning = None
        self.draw = 0
        self.p1 = None
        self.p2 = None

        ''' add input into player()
            if input is bot, then PvB
            '''

    def start(self):
        if self.game_count == 0:
            self.p1 = Players(input('Enter Username: ').upper())
            self.p2 = Players("BOT FRED")
        else:
            self.p1 = Players(self.p1.name, self.p1.score)
            self.p2 = Players(self.p2.name, self.p2.score)

        Round(self.p1, self.p2)
        self.game_count += 1

    def determine_winner(self, result):
        winner_dict = {
            -1: f'The winner is {self.p2.name}!',
            0: f'The result is a draw!',
            1: f'The winner is {self.p1.name}!'
            }
        score_dict = {
            -1: [0, 1],
            0: [0, 0],
            1: [1, 0]
            }
        self.p1.score += score_dict[result][0]
        self.p2.score += score_dict[result][1]

        if self.p1.score > self.p2.score:
            self.winning = self.p1.name
        elif self.p1.score < self.p2.score:
            self.winning = self.p2.name
        else:
            self.winning = 'No one! it\'s a tie!'
            self.draw +=1

        print(f'{self.p2.name} chose {self.p2.input}')
        print(winner_dict[result])

    @staticmethod
    def play_again():
        another_game = input('Do you want to play again? ').upper()
        if another_game in ['YES', 'Y', 'YH', 'YEP']:
            return True

    def end_game(self):
        print(
            f'\nThe Final scores after {self.game_count} games are: \n{self.p1.name}: '
            f'{self.p1.score} \n{self.p2.name}: {self.p2.score}\nDraws: {self.draw}')
        print(
            f'The winner is {self.winning}')


keep_playing = True
Game = Game()
while keep_playing:
    Game.start()
    if not Game.play_again():
        keep_playing = False

Game.end_game()


