'''
13"51
'''

# TODO: fix the placement of the ship. CUrrent it snaps to the grid but only to where the mouse
#  is let go. It should be at a regular intervals along the ship image. i.e. for the carrier of
#  length 200 pxs there should be 5 lockable positionson the ship at every 40 px for example...
#  idea: Maybe find where mouse is on the rectangle and find the closest value to it. then center
#  the rect on the mouse adjusted for the closest point hcosen. THEN SNAP??

import os
import sys
import time
import numpy
import pygame as pg
from pygame.locals import K_q
from scipy import spatial


CAPTION = "Place Ships"
SCREEN_SIZE = _WIDTH, _HEIGHT = 750, 750
_BLACK = (0, 0, 0)
_GREY = (160, 160, 160)
_WHITER = (225, 225, 225)

_BOX = (60, 60, _WIDTH / 1.5, _HEIGHT / 1.5)
image_dir = os.path.dirname(sys.argv[0]) + '\\images\\'



class Ships(object):

    def __init__(self, image, start_pos, HP, size):
        self.image = pg.transform.scale(pg.image.load(image), size).convert()
        self.rectangle = self.image.get_rect()
        self.rectangle.centerx = start_pos[0]
        self.rectangle.top = start_pos[1]
        self.position = []
        # self.click_carrier = False
        self.ship_hp = HP
        # self.carrier_vert = True
        # self.carrier_on_grid = False
        self.ship_booleans = {'click_carrier': False, 'vertical': True, 'On_Grid': False}


    @staticmethod
    def _size_ship(ship):
        _SIZE_SHIP = {'CARRIER': ((_BOX[2] - _BOX[0] - 40) / 10, 5 * ((_BOX[3]) / 10) - 4),
                      'DESTROYER': ((_BOX[2] - _BOX[0] - 40) / 10, 2 * ((_BOX[3]) / 10) - 4)}
        return _SIZE_SHIP[ship]


class Character(object):
    """
    A class to represent our lovable red sqaure.
    """
    SIZE = ((_BOX[2] - _BOX[0] - 40) / 10, 4 * ((_BOX[3]) / 10) - 4)

    def __init__(self, pos):
        """
        The argument pos corresponds to the center of our rectangle.
        """

        self.grid = self.get_grid_positions(_BOX)
        self.carrier_ship = Ships(image_dir + 'pirate-ship.png', (600, 60), 5,
                                  Ships._size_ship('CARRIER'))

        self.destroyer_ship = Ships(image_dir + 'destroyer.png',
                                    (660, 60), 2, Ships._size_ship('DESTROYER'))
        self.fleet = [self.carrier_ship,self.destroyer_ship]

    def setup_font(self):
        """
        If your text doesn't change it is best to render once, rather than
        re-render every time you want the text.  Rendering text every frame is
        a common source of bottlenecks in beginner programs.
        """
        font = pg.font.SysFont('timesnewroman', 15)
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

        if self.carrier_ship.rectangle.collidepoint(pos):
            self.carrier_ship.ship_booleans['click_carrier'] = True
            pg.mouse.get_rel()
        elif self.destroyer_ship.rectangle.collidepoint(pos):
            self.destroyer_ship.ship_booleans['click_carrier'] = True
            pg.mouse.get_rel()

    def find_nearest(self, pos=()):
        dictn = self.grid
        if not pos:
            pos = pg.mouse.get_pos()
        dict_strcorrd = {coord_str: dictn[coord_str][4] for coord_str in dictn}
        list_of_center = [dictn[coord_str][4] for coord_str in dictn]
        tree = spatial.KDTree(list_of_center)
        match = tree.query([(pos[0], pos[1])])
        result = list(dict_strcorrd.keys())[
            list(dict_strcorrd.values()).index(list_of_center[match[1][0]])]

        return result

    def update(self, screen_rect):
        """
        If the square is currently clicked, update its position based on the
        relative mouse movement.  Clamp the rect to the screen.
        """

        if self.carrier_ship.ship_booleans['click_carrier']:
            self.carrier_ship.rectangle.move_ip(pg.mouse.get_rel())
            self.carrier_ship.rectangle.clamp_ip(screen_rect)

        elif self.destroyer_ship.ship_booleans['click_carrier']:
            self.destroyer_ship.rectangle.move_ip(pg.mouse.get_rel())
            self.destroyer_ship.rectangle.clamp_ip(screen_rect)

    def draw(self, surface):
        """
        Blit image and text to the target surface.
        """
        surface.blit(self.carrier_ship.image,
                     self.carrier_ship.rectangle)
        surface.blit(self.destroyer_ship.image,
                     self.destroyer_ship.rectangle)

    def drawgrid(self, surface, grid_main):

        start = (grid_main[0], grid_main[1])
        end = (grid_main[2], grid_main[3])
        # pygame.draw.rect(_VARS['surf'], _WHITER, (start, end), )
        # pygame.draw.rect(_VARS['surf'], _BLACK, (start, end), 1)

        for i in range(11):
            # vert change x
            pg.draw.line(surface, (255, 255, 255), (start[0] + (i * end[0] / 10), start[1]),
                         (start[0] + (i * end[0] / 10), end[1] + start[1]), 2)
            # horizontal change y
            pg.draw.line(surface, (255, 255, 255), (start[0], start[1] + (i * end[0] / 10)),
                         (end[0] + start[0], start[1] + (i * end[0] / 10)), 2)

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
                                     start[1] + 5 + (k * end[0] / 10),
                                     (end[0] / 10) - 8, (end[0] / 10) - 8, (x, y)]
        return grid

    def snaptocoord(self, ship_obj):
        result = self.find_nearest(ship_obj.rectangle.center)

        if ship_obj.ship_booleans['vertical']:
            if ship_obj.ship_hp % 2 == 0:
                if (ship_obj.rectangle.centery - self.grid[result][4][1]) <= 0:
                    ship_obj.rectangle.centery = self.grid[result][4][1] - (self.grid[result][3] / 2) - 4
                else:
                    ship_obj.rectangle.centery = self.grid[result][4][1] + (self.grid[result][3] / 2) + 4
                ship_obj.rectangle.centerx = self.grid[result][4][0]

            else:  # odd ship length and is vertical

                ship_obj.rectangle.centerx = self.grid[result][4][0]
                ship_obj.rectangle.centery = self.grid[result][4][1]

            if ship_obj.rectangle.top < _BOX[0]:
                ship_obj.rectangle.top = _BOX[0] + 2
            elif ship_obj.rectangle.bottom > _BOX[1] + _BOX[3]:
                ship_obj.rectangle.bottom = _BOX[0] + _BOX[3] - 1

        elif not ship_obj.ship_booleans['vertical']:

            if ship_obj.ship_hp % 2 == 0:
                if (ship_obj.rectangle.centerx - self.grid[result][4][0]) <= 0:
                    ship_obj.rectangle.centerx = self.grid[result][4][0] - (self.grid[result][2] / 2) - 4
                else:
                    ship_obj.rectangle.centerx = self.grid[result][4][0] + (self.grid[result][2] / 2) + 4
                ship_obj.rectangle.centery = self.grid[result][4][1]

            else:  # odd ship length and is vertical
                ship_obj.rectangle.centery = self.grid[result][4][1]
                ship_obj.rectangle.centerx = self.grid[result][4][0]

            if ship_obj.rectangle.right > _BOX[0] + _BOX[2]:  # #  #  #
                ship_obj.rectangle.right = _BOX[0] + _BOX[2] - 2  #
            elif ship_obj.rectangle.left < _BOX[0]:  #
                ship_obj.rectangle.left = _BOX[0] + 2

    def rotate(self, ship_obj, surface):

        ship_obj.ship_booleans['vertical'] = not ship_obj.ship_booleans['vertical']

        mx, my = pg.mouse.get_pos()
        ship_obj.image = pg.transform.rotate(ship_obj.image, 90)
        ship_obj.rectangle = ship_obj.image.get_rect()
        ship_obj.rectangle.center = (mx, my)
        surface.blit(ship_obj.image, ship_obj.rectangle)

    def ship_overlap(self, screen,fleet):
        for j, ship_obj in enumerate(fleet):
            overlap = []
            for i in self.grid:
                r = pg.Rect.colliderect(ship_obj.rectangle, self.grid[i][:4])
                if r is True:
                    overlap.append(i)
            ship_obj.position = overlap

            font = pg.font.SysFont('arial', 15)
            label1 = font.render(f'overlap: {ship_obj.position}', True, _BLACK)
            rect = label1.get_rect()
            pg.draw.rect(screen, _GREY, [100, 600 + (20*j), rect[2] * 1, rect[3] * 1.3], )
            screen.blit(label1, (100, 600 + (20*j)))

        # print(self.carrier_ship.position)

    def show_mouse_where(self, screen):
        mouse = pg.mouse.get_pos()
        font = pg.font.SysFont('arial', 20)
        label = font.render(f'x: {mouse[0]} y: {mouse[1]}', True, _BLACK)
        label1 = font.render(f'x: 999 y: 999', True, _BLACK)
        rect = label1.get_rect()
        pg.draw.rect(screen, _GREY, [rect[0], rect[1], rect[2] * 1.3, rect[3] * 1.3], )
        screen.blit(label, (0, 0))

    def display_coord(self, Coord, screen):
        mouse = pg.mouse.get_pos()
        font = pg.font.SysFont('arial', 15)
        label1 = font.render(f'pos: {Coord} - {self.grid[Coord][:4]}', True, _BLACK)
        rect = label1.get_rect()
        if _BOX[0] < mouse[0] < (_BOX[2] + _BOX[0]) and _BOX[1] < mouse[1] < (_BOX[3] + _BOX[1]):
            pg.draw.rect(screen, _GREY, [250, 0, rect[2] * 1, rect[3] * 1.3], )
            screen.blit(label1, (250, 0))


class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """

    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our player (draggable rect).
        """
        self.screen = pg.display.get_surface()  # display screen
        self.screen_rect = self.screen.get_rect()  # displat screen rectangle
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
        self.mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.player.check_click(event.pos)

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for ship in self.player.fleet:
                    if ship.ship_booleans['click_carrier'] == True :
                        ship.ship_booleans['click_carrier'] = False
                        self.player.snaptocoord(ship)
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                for ship_obj in self.player.fleet:
                    if event.key == pg.K_r and ship_obj.ship_booleans['click_carrier'] == True:
                        self.player.rotate(ship_obj, self.screen)
                        print('rotate')

                if event.key == K_q:
                    print('q pressed')
                    self.boo = True

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(_GREY)
        self.player.drawgrid(self.screen, _BOX)
        self.player.show_mouse_where(self.screen)
        self.player.ship_overlap(self.screen,self.player.fleet)
        self.player.draw(self.screen)

        self.player.display_coord(self.player.find_nearest(), self.screen)

        pg.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
        while not self.done:
            self.event_loop()

            if not self.boo:
                # print(self.player.carrier.center)
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
