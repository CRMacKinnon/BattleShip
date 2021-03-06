import sys
import os
import pygame
from pygame.locals import KEYDOWN, K_q
from scipy import spatial

dir = os.path.dirname(sys.argv[0])
_SCREENSIZE = _WIDTH, _HEIGHT = 750, 750
_BLACK = (0, 0, 0)
_GREY = (160, 160, 160)
_WHITER = (225, 225, 225)
_VARS = {
    'surf': False
    }
PADDING = 20
_BOX = (60, 60, _WIDTH/1.6, _HEIGHT/1.6)

# This is the main game loop, it constantly runs until you press the Q KEY
# or close the window.
# CAUTION: THis will run as fast as you computer allows,
# if you need to set a specific FPS look at tick methods.

def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(_SCREENSIZE)
    drawrect(_BOX)
    grid_hit_squares_dict = get_grid_positions(_BOX)
    # print(grid_hit_squares_dict)

    img = pygame.transform.scale(pygame.image.load('/Users/cal/Downloads/pirate-ship.png'),
                                   (30,30)).convert()
    rect = img.get_rect()
    rect.center = rect[2]/2, rect[3]/2
    moving = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if rect.collidepoint(event.pos):
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False

                mouse = pygame.mouse.get_pos()

                result = find_nearest(mouse[0],mouse[1],grid_hit_squares_dict)
                rect.x=grid_hit_squares_dict[result][4][0] - 15
                rect.y = grid_hit_squares_dict[result][4][1] -15


                pygame.display.update()

                # Make your image move continuously
            elif event.type == pygame.MOUSEMOTION and moving:
                rect.move_ip(event.rel)

        _VARS['surf'].fill(_GREY)
        drawrect(_BOX)

        _VARS['surf'].blit(img, rect)

        show_mouse_where(grid_hit_squares_dict)
        find_nearest(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],grid_hit_squares_dict)
        pygame.display.update()


def highlightship(dictn,l):

    grid = _BOX
    mouse = pygame.mouse.get_pos()
    result = find_nearest(mouse[0],mouse[1],dictn)
    x0,y0,x1,y1 = dictn[result][0],dictn[result][1],dictn[result][2] + dictn[result][0],dictn[result][3] + dictn[result][1]
    letters =list('ABCDEFGHIJ')
    letters = letters[::-1]
    while letters[0] != result[0]:
        letters.append(letters.pop(0))

    for ship, let in zip(range(l), letters):
        pygame.draw.rect(_VARS['surf'],(0, 66, 100), dictn[f'{let}{result[1]}'][:4])

        
    # if x0 <= mouse[0] <= x1 and y0 <= mouse[1] <= y1:
    #     for ship,let in zip(range(5),letters):
    #
    #         pygame.draw.rect(_VARS['surf'],(0, 66, 100),dictn[f'{let}{result[1]}'][:4])


def mouse_click(dictn):

    pos = pygame.mouse.get_pos()
    result = find_nearest(pos[0], pos[1], dictn)

    pygame.draw.rect(_VARS['surf'], _BLACK, dictn[result][:4])


def snap_mouse(dictn):
    grid = _BOX
    mouse = pygame.mouse.get_pos()
    if grid[0] < mouse[0] < (grid[0] + grid[3]) and grid[1] < mouse[1] < (grid[1] + grid[2]):
        result = find_nearest(mouse[0], mouse[1], dictn)
        # print(dictn[result][4])
        pygame.mouse.set_pos(dictn[result][4])


def find_nearest(mx, my, dictn):


    dict_strcorrd = {coord_str: dictn[coord_str][4] for coord_str in dictn}
    list_of_center = [dictn[coord_str][4] for coord_str in dictn]
    tree = spatial.KDTree(list_of_center)
    match = tree.query([(mx, my)])
    result = list(dict_strcorrd.keys())[
        list(dict_strcorrd.values()).index(list_of_center[match[1][0]])]

    font = pygame.font.SysFont('arial', 35)
    label1 = font.render(f'pos: {result}', True, _BLACK)
    # label1 = font.render(f'pos: {result}', True, _BLACK)

    rect = label1.get_rect()
    if 60 < mx <  (_BOX[2] + 60)  and 60 < my <  (_BOX[3] + 60) :
        pygame.draw.rect(_VARS['surf'], _GREY, [250, 0, rect[2] * 1, rect[3] * 1.3], )
        _VARS['surf'].blit(label1, (250, 0))


def show_mouse_where(dictn):
    mouse = pygame.mouse.get_pos()
    font = pygame.font.SysFont('arial', 35)
    label = font.render(f'x: {mouse[0]} y: {mouse[1]}', True, _BLACK)
    label1 = font.render(f'x: 999 y: 999', True, _BLACK)
    rect = label1.get_rect()
    pygame.draw.rect(_VARS['surf'], _GREY, [rect[0], rect[1], rect[2] * 1.3, rect[3] * 1.3], )
    _VARS['surf'].blit(label, (0, 0))


def get_grid_positions(grid_main):
    grid = {}


    start = (grid_main[0], grid_main[1])
    end = (grid_main[2], grid_main[3])
    for xbox, LET in zip(range(10), list('ABCDEFGHIJ')):
        for ybox in range(10):

            x = (2 * (start[0] + 5 + (ybox * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
            y = (2 * (start[1] + 5 + (xbox * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
            r = (x ** 2 + y ** 2) ** 0.5

            grid[f'{LET}{ybox}'] = [start[0] + 5 + (xbox * end[0] / 10), start[1] + 5 + (ybox *
                                                                                          end[
                0] / 10),
                                 (end[0] / 10) - 8, (end[0] / 10) - 8, (x, y),False]
    return grid


def changegrid(coord, grid):
    pygame.draw.rect(_VARS['surf'], _BLACK, grid[coord][:4])


def drawrect(grid_main):
    start = (grid_main[0], grid_main[1])
    end = (grid_main[2], grid_main[3])
    pygame.draw.rect(_VARS['surf'], (53, 138, 202), (start, end), )

    for i in range(11):
        # vert change x
        pygame.draw.line(_VARS['surf'],
                         _BLACK,
                         (start[0] + (i * end[0] / 10), start[1]),
                         (start[0] + (i * end[0] / 10), end[1] + start[1]),
                         2)
        # horizontal change y
        pygame.draw.line(_VARS['surf'],
                         _BLACK,
                         (start[0], start[1] + (i * end[0] / 10)),
                         (end[0] + start[0], start[1] + (i * end[0] / 10)),
                         2)


def checkevents(dictn):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_click(dictn)


if main() == '__main__':
    main()
