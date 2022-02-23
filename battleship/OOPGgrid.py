"""
A very simple example showing how to drag an item with the mouse.
Dragging in this example uses relative mouse movement.
-Written by Sean J. McKiernan 'Mekire'
"""

# TODO: fix the placement of the ship. CUrrent it snaps to the grid but only to where the mouse
#  is let go. It should be at a regular intervals along the ship image. i.e. for the carrier of
#  length 200 pxs there should be 5 lockable positionson the ship at every 40 px for example...
#  idea: Maybe find where mouse is on the rectangle and find the closest value to it. then center
#  the rect on the mouse adjusted for the closest point hcosen. THEN SNAP??
import os
import sys
import time

import pygame as pg
from pygame.locals import K_q
from scipy import spatial

CAPTION = "Place Ships"
SCREEN_SIZE = _WIDTH, _HEIGHT = 750, 750
_BLACK = (0, 0, 0)
_GREY = (160, 160, 160)
_WHITER = (225, 225, 225)

_BOX = (60, 60, _WIDTH / 1.6, _HEIGHT / 1.6)


class Character(object):
    """
    A class to represent our lovable red sqaure.
    """
    SIZE = ((_BOX[2] - _BOX[0] - 40) / 10, 5.2 * ((_BOX[3] - _BOX[1]) / 10))

    def __init__(self, pos):
        """
        The argument pos corresponds to the center of our rectangle.
        """

        self.grid = self.get_grid_positions(_BOX)

        self.carrier_img = pg.transform.scale(pg.image.load(
            '/Users/cal/downloads/pirate-ship.png'),Character.SIZE).convert()
        self.carrier = self.carrier_img.get_rect()

        self.carrier.center = (600, 60)
        self.click_carrier = False
        self.carrier_vert = True

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
        # if self.rect.collidepoint(pos):
        #     self.click = True
        #     pg.mouse.get_rel()
        if self.carrier.collidepoint(pos):
            self.click_carrier = True
            pg.mouse.get_rel()

    def find_nearest(self):
        dictn = self.grid
        mx, my = pg.mouse.get_pos()
        dict_strcorrd = {coord_str: dictn[coord_str][4] for coord_str in dictn}
        list_of_center = [dictn[coord_str][4] for coord_str in dictn]
        tree = spatial.KDTree(list_of_center)
        match = tree.query([(mx, my)])
        result = list(dict_strcorrd.keys())[
            list(dict_strcorrd.values()).index(list_of_center[match[1][0]])]

        return result

    def update(self, screen_rect):
        """
        If the square is currently clicked, update its position based on the
        relative mouse movement.  Clamp the rect to the screen.
        """

        if self.click_carrier:
            self.carrier.move_ip(pg.mouse.get_rel())
            self.carrier.clamp_ip(screen_rect)

            # self.snaptocoord()

    def draw(self, surface):
        """
        Blit image and text to the target surface.
        """
        surface.blit(self.carrier_img, self.carrier)
        # surface.fill(pg.Color("white"), self.carrier)  # surface.blit(self.text, self.text_rect)

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

    def snaptocoord(self, ship):

        result = self.find_nearest()
        x,y,w,h = self.carrier
        # corners = [(x,y),(x+w,y),(x,y+h),(x+w,y+h)]
        mx,my = pg.mouse.get_pos()
        # rel_grab =
        # ship.x = self.grid[result][4][0] - (Character.SIZE[0] / 2)
        if self.carrier_vert == True:
            ship.y = self.grid[result][4][1] - (Character.SIZE[1] / 2) - (my - self.carrier.centery)
            ship.x = self.grid[result][4][0] - (Character.SIZE[0] / 2)
        elif self.carrier_vert == False:
            ship.y = self.grid[result][4][1] - (Character.SIZE[0] / 2) - (my - self.carrier.centery)
            ship.x = self.grid[result][4][0] - (Character.SIZE[1] / 2)+ ( self.carrier.centerx - mx)




    def rotate(self, ship,surface):

        self.carrier_vert = not self.carrier_vert
        print(self.carrier_vert)
        mx,my = pg.mouse.get_pos()
        self.carrier_img = pg.transform.rotate(self.carrier_img, 90)
        self.carrier = self.carrier_img.get_rect()
        self.carrier.center = (mx,my)
        surface.blit(self.carrier_img, self.carrier)


    def show_mouse_where(self,screen):
        mouse = pg.mouse.get_pos()
        font = pg.font.SysFont('arial', 35)
        label = font.render(f'x: {mouse[0]} y: {mouse[1]}', True, _BLACK)
        label1 = font.render(f'x: 999 y: 999', True, _BLACK)
        rect = label1.get_rect()
        pg.draw.rect(screen, _GREY, [rect[0], rect[1], rect[2] * 1.3, rect[3] * 1.3], )
        screen.blit(label, (0, 0))


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
                self.player.click_carrier = False
                self.player.snaptocoord(self.player.carrier)
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                if event.key == pg.K_r and  self.player.click_carrier == True:
                    self.player.rotate(self.player.carrier_img,self.screen)
                    print('rotate')


                if event.key == K_q:
                    print('q pressed')
                    self.boo = True

    def find_nearest(self, mx, my, dictn):
        dictn = self.player.grid
        dict_strcorrd = {coord_str: dictn[coord_str][4] for coord_str in dictn}
        list_of_center = [dictn[coord_str][4] for coord_str in dictn]
        tree = spatial.KDTree(list_of_center)
        match = tree.query([(mx, my)])
        result = list(dict_strcorrd.keys())[
            list(dict_strcorrd.values()).index(list_of_center[match[1][0]])]

        return result

    def display_coord(self, Coord):
        font = pg.font.SysFont('arial', 35)
        label1 = font.render(f'pos: {Coord}', True, _BLACK)
        rect = label1.get_rect()
        if _BOX[0] < self.mouse[0] < (_BOX[2] + _BOX[0]) and _BOX[1] < self.mouse[1] < (
                _BOX[3] + _BOX[1]):
            pg.draw.rect(self.screen, _GREY, [250, 0, rect[2] * 1, rect[3] * 1.3], )
            self.screen.blit(label1, (250, 0))

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(_GREY)
        self.player.show_mouse_where(self.screen)
        self.player.draw(self.screen)

        self.player.drawgrid(self.screen, _BOX)
        self.display_coord(self.find_nearest(self.mouse[0], self.mouse[1], self.player.grid))

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
