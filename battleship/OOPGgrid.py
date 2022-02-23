"""
A very simple example showing how to drag an item with the mouse.
Dragging in this example uses relative mouse movement.
-Written by Sean J. McKiernan 'Mekire'
"""
import os
import sys
import time

import pygame as pg
from pygame.locals import K_q
from scipy import spatial

CAPTION = "Drag the Red Square"
SCREEN_SIZE = (750, 750)


class Character(object):
    """
    A class to represent our lovable red sqaure.
    """
    SIZE = (150, 150)

    def __init__(self, pos):
        """
        The argument pos corresponds to the center of our rectangle.
        """
        self.rect = pg.Rect((0, 0), Character.SIZE)
        self.rect.center = pos
        self.text, self.text_rect = self.setup_font()
        self.click = False
        self.grid = self.get_grid_positions([30, 30, 300,
                                             300])  # self.carrier = ShipInfo('Carrier', 'Ca', 5,
        # 'green')  # self.battleship = ShipInfo('Battleship', 'Bt', 4, 'yellow')  # self.cruiser
        # = ShipInfo('Cruiser', 'Cr', 3, 'blue')  # self.submarine = ShipInfo('Submarine', 'Sb',
        # 3, 'magenta')  # self.destroyer = ShipInfo('Destroyer', 'Dy', 2, 'cyan')

    def setup_font(self):
        """
        If your text doesn't change it is best to render once, rather than
        re-render every time you want the text.  Rendering text every frame is
        a common source of bottlenecks in beginner programs.
        """
        font = pg.font.SysFont('timesnewroman', 30)
        message = "I'm a red square"
        label = font.render(message, True, pg.Color("white"))
        label_rect = label.get_rect()
        return label, label_rect

    def check_click(self, pos):
        """
        This function is called from the event loop to check if a click
        overlaps with the player rect.
        pygame.mouse.get_rel must be called on an initial hit so that
        subsequent calls give the correct relative offset.
        """
        if self.rect.collidepoint(pos):
            self.click = True
            pg.mouse.get_rel()

    def find_nearest(self, mx, my, dictn):

        dict_strcorrd = {coord_str: dictn[coord_str][4] for coord_str in dictn}
        list_of_center = [dictn[coord_str][4] for coord_str in dictn]
        tree = spatial.KDTree(list_of_center)
        match = tree.query([(mx, my)])
        result = list(dict_strcorrd.keys())[
            list(dict_strcorrd.values()).index(list_of_center[match[1][0]])]
        # print(f'match: {match[1]}:{result}')
        return result

    def update(self, screen_rect):
        """
        If the square is currently clicked, update its position based on the
        relative mouse movement.  Clamp the rect to the screen.
        """
        if self.click:
            self.rect.move_ip(pg.mouse.get_rel())
            self.rect.clamp_ip(screen_rect)

        self.text_rect.center = (self.rect.centerx, self.rect.centery + 90)

    def draw(self, surface):
        """
        Blit image and text to the target surface.
        """
        surface.fill(pg.Color("white"), self.rect)
        surface.blit(self.text, self.text_rect)

    def drawgrid(self, surface, grid_main):

        start = (grid_main[0], grid_main[1])
        end = (grid_main[2], grid_main[3])
        # pygame.draw.rect(_VARS['surf'], _WHITER, (start, end), )
        # pygame.draw.rect(_VARS['surf'], _BLACK, (start, end), 1)

        for i in range(11):
            # vert change x
            pg.draw.line(surface,
                         (255, 255, 255),
                         (start[0] + (i * end[0] / 10), start[1]),
                         (start[0] + (i * end[0] / 10), end[1] + start[1]),
                         2)
            # horizontal change y
            pg.draw.line(surface,
                         (255, 255, 255),
                         (start[0], start[1] + (i * end[0] / 10)),
                         (end[0] + start[0], start[1] + (i * end[0] / 10)),
                         2)

    def get_grid_positions(self, grid_main):
        grid = {f'{j}{i}': '' for i in range(10) for j in list('ABCDEFGHIJ')}

        start = (grid_main[0], grid_main[1])
        end = (grid_main[2], grid_main[3])
        for k, LET in zip(range(10), list('ABCDEFGHIJ')):
            for j in range(10):

                x = (2 * (start[0] + 5 + (j * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
                y = (2 * (start[1] + 5 + (k * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
                r = (x ** 2 + y ** 2) ** 0.5

                grid[f'{LET}{j}'] = [start[0] + 5 + (j * end[0] / 10),
                                     start[1] + 5 + (k * end[0] / 10), (end[0] / 10) - 8,
                                     (end[0] / 10) - 8, (x, y)]
        return grid


class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """

    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our player (draggable rect).
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Character(self.screen_rect.center)
        self.boo = False
        self.playgame = False

    def event_loop(self):
        """
        This is the event loop for the whole program.
        Regardless of the complexity of a program, there should never be a need
        to have more than one event loop.
        """
        for event in pg.event.get():

            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.player.check_click(event.pos)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.player.click = False
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                print('pressed')

                if event.key == K_q:
                    print('q pressed')
                    self.boo = True

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pg.Color("black"))
        self.player.draw(self.screen)
        self.player.drawgrid(self.screen, [30, 30, 300, 300])
        # result = self.find_nearest(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], self.grid)
        # self.rect.move_ip(self.grid[result][4])
        pg.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
        while not self.done:
            self.event_loop()
            if not self.boo:
                print(self.boo)
                self.player.update(self.screen_rect)
                self.render()
                self.clock.tick(self.fps)
            if self.boo is True and self.playgame is not True:
                ''' Here place the ships
                '''
                self.screen.fill((0, 0, 0))
                self.playgame = True
                pg.display.update()
                time.sleep(1.5)
            if self.playgame is True:
                '''Here play game
                '''
                self.screen.fill((255, 0, 0))
                pg.display.update()


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    print('end')
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
