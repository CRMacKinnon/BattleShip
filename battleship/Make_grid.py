import sys

import pygame
from pygame.locals import KEYDOWN, K_q
from scipy import spatial

_SCREENSIZE = _WIDTH, _HEIGHT = 750, 750
_BLACK = (0, 0, 0)
_GREY = (160, 160, 160)
_WHITER = (225, 225, 225)
_VARS = {
    'surf': False
    }
PADDING = 20


# This is the main game loop, it constantly runs until you press the Q KEY
# or close the window.
# CAUTION: THis will run as fast as you computer allows,
# if you need to set a specific FPS look at tick methods.

def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(_SCREENSIZE)
    _VARS['surf'].fill(_GREY)
    drawrect((60, 60, _WIDTH / 1.5, _HEIGHT / 1.5))
    grid_hit_squares_dict = get_grid_positions((60, 60, _WIDTH / 1.5, _HEIGHT / 1.5))
    grid_hit_center = {coord_str: grid_hit_squares_dict[coord_str][4] for coord_str in
                       grid_hit_squares_dict}

    while True:
        checkevents(grid_hit_squares_dict)
        # changegrid('J9', grid_hit_squares_dict)

        # mouse_click(grid_hit_squares_dict)

        show_mouse_where(grid_hit_squares_dict)
        # snap_mouse(grid_hit_squares_dict)
        pygame.display.update()


def mouse_click(evnt, dictn):
    if evnt.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        result = find_nearest(pos[0], pos[1], dictn)
        print(result)
        pygame.draw.rect(_VARS['surf'], _BLACK, dictn[result][:4])


def snap_mouse(dictn):
    grid = (60, 60, _WIDTH / 1.5, _HEIGHT / 1.5)
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
    # print(f'match: {match[1]}:{result}')
    return result


def show_mouse_where(dictn):
    mouse = pygame.mouse.get_pos()
    font = pygame.font.SysFont('arial', 35)
    label = font.render(f'x: {mouse[0]} y: {mouse[1]}', True, _BLACK)
    rect = label.get_rect()
    pygame.draw.rect(_VARS['surf'], _GREY, [rect[0], rect[1], rect[2] * 1.3, rect[3] * 1.3], )
    _VARS['surf'].blit(label, (0, 0))


def get_grid_positions(grid_main):
    grid = {f'{j}{i}': '' for i in range(10) for j in list('ABCDEFGHIJ')}

    start = (grid_main[0], grid_main[1])
    end = (grid_main[2], grid_main[3])
    for k, LET in zip(range(10), list('ABCDEFGHIJ')):
        for j in range(10):

            x = (2 * (start[0] + 5 + (j * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
            y = (2 * (start[1] + 5 + (k * end[0] / 10)) + ((end[0] / 10) - 8)) / 2
            r = (x ** 2 + y ** 2) ** 0.5

            grid[f'{LET}{j}'] = [start[0] + 5 + (j * end[0] / 10), start[1] + 5 + (k * end[0] / 10),
                                 (end[0] / 10) - 8, (end[0] / 10) - 8, (x, y)]
    return grid


def changegrid(coord, grid):
    pygame.draw.rect(_VARS['surf'], _BLACK, grid[coord][:4])


def drawrect(grid_main):
    start = (grid_main[0], grid_main[1])
    end = (grid_main[2], grid_main[3])
    # pygame.draw.rect(_VARS['surf'], _WHITER, (start, end), )
    # pygame.draw.rect(_VARS['surf'], _BLACK, (start, end), 1)

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
        mouse_click(event, dictn)


if main() == '__main__':
    main()
