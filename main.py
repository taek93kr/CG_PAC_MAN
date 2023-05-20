import random
import math
import copy
import pygame
import sys
import warnings
# https://shaunlebron.github.io/pacman-mazegen/
# https://blockdmask.tistory.com/570

warnings.filterwarnings('ignore', category=Warning)

G_BLOCK_SIZE = 32
G_WORLD_SIZE_W = random.randint(5, 10)
G_WORLD_SIZE_H = random.randint(5, 10)
G_WORLD_SIZE_W = 15
G_WORLD_SIZE_H = 15
G_FPS = 120

class Ghost:
    def __init__(self, x, y):
        self.m_pos = [x, y]
        self.m_init_pos = [x, y]
        self.m_type = random.randint(1, 5)
        self.m_face = 0 # 0:Left 1:Right
        self.m_out = 0
        self.m_img = []
        self.m_img.append(pygame.image.load('images/ghost%dr.png' % self.m_type))
        self.m_img.append(pygame.image.load('images/ghost%d.png' % self.m_type))
        self.m_img.append(pygame.image.load('images/ghost_whiter.png'))
        self.m_img.append(pygame.image.load('images/ghost_white.png'))
        self.m_img.append(pygame.image.load('images/ghost%dr.png' % self.m_type))
        self.m_img.append(pygame.image.load('images/ghost%d.png' % self.m_type))

        self.m_mode = 0 # 0:strong 1:week 2:revival
        self.m_mode_tick = 0
        self.m_speed = [1, 1, 3]
        self.m_direction = 0 # 0:l 1:r 2:u :3:d

    def move(self, maze):
        # if '|' not in self.blocks_ahead_of(maze, 0, random.randint(0, 1)):
        #     # self.m_pos[0] += self.m_speed[self.m_mode]
        #     self.m_pos[0] += 0.1
        # if '|' not in self.blocks_ahead_of(maze, 1, random.randint(0, 1)):
        #     # self.m_pos[1] += self.m_speed[self.m_mode]
        #     self.m_pos[1] += 0.1
        # pass
        if self.m_mode == 2:
            self.m_mode_tick -= 1
            if self.m_mode_tick == 0:
                self.m_mode = 0
            return

        o_x = self.m_pos[0]
        o_y = self.m_pos[1]

        wall_list = ['|']
        if self.m_out:
            wall_list.append('x')

        chance = self.m_speed[self.m_mode]
        while chance:
            x_avail = False
            y_avail = False
            # Check direction
            avail = [0, 0, 0, 0]
            d = 50  # 1 2 4 5 10 20 50 100

            # 방향 있음 -> 20% 확률로 반대
            # 방향 없음 -> 50% 확률로 방향 선택
            if self.m_pos[1] % 100 == 0: # check x_avail
                if self.m_pos[0] % 100 == 0:
                    x = int(self.m_pos[0]/100)
                    y = int(self.m_pos[1]/100)
                    if x > 1 and not maze[y][x - 1] in wall_list:
                        avail[0] = 1 # left
                    if x < G_WORLD_SIZE_W * 2 - 2 and not maze[y][x + 1] in wall_list:
                        avail[1] = 1 # right
                else:
                    avail[0] = 1 # left
                    avail[1] = 1 # right
            else:
                avail[2] = 1
                avail[3] = 1
            if self.m_pos[0] % 100 == 0: # check y_avail
                if self.m_pos[1] % 100 == 0:
                    x = int(self.m_pos[0]/100)
                    y = int(self.m_pos[1]/100)
                    if y > 1 and not maze[y - 1][x] in wall_list:
                        avail[2] = 1 # up
                    if y < G_WORLD_SIZE_W - 1 and not maze[y + 1][x] in wall_list:
                        avail[3] = 1 # down
                else:
                    avail[2] = 1 # up
                    avail[3] = 1 # down
            else:
                avail[0] = 1
                avail[1] = 1
            x_avail = (avail[0] or avail[1])
            y_avail = (avail[2] or avail[3])

            axis = random.randint(0, 1)
            direct = random.randint(0, 1)
            if self.m_pos[0] % 100 == 0 and self.m_pos[1] % 100 == 0:
                if x_avail and y_avail:
                    if axis: # x
                        if avail[0] and avail[1]:
                            if direct: # [+]
                                self.m_pos[0] += d
                                self.m_direction = 1
                            else:
                                self.m_pos[0] -= d
                                self.m_direction = 0
                        elif avail[0]:
                            self.m_pos[0] -= d
                            self.m_direction = 0
                        else:
                            self.m_pos[0] += d
                            self.m_direction = 1
                    else:
                        if avail[2] and avail[3]:
                            if direct: # [+]
                                self.m_pos[1] += d
                                self.m_direction = 3
                            else:
                                self.m_pos[1] -= d
                                self.m_direction = 2
                        elif avail[2]:
                            self.m_pos[1] -= d
                            self.m_direction = 2
                        else:
                            self.m_pos[1] += d
                            self.m_direction = 3
                elif x_avail:
                    if avail[0] and avail[1]:
                        if direct: # [+]
                            self.m_pos[0] += d
                        else:
                            self.m_pos[0] -= d
                    elif avail[0]:
                        self.m_pos[0] -= d
                    else:
                        self.m_pos[0] += d
                elif y_avail:
                    if avail[2] and avail[3]:
                        if direct: # [+]
                            self.m_pos[1] += d
                        else:
                            self.m_pos[1] -= d
                    elif avail[2]:
                        self.m_pos[1] -= d
                    else:
                        self.m_pos[1] += d
            elif self.m_direction == 0: # left
                direct = random.randint(1, 100)
                if direct > 1:
                    self.m_pos[0] -= d
                else:
                    self.m_pos[0] += d
            elif self.m_direction == 1: # right
                direct = random.randint(1, 100)
                if direct > 1:
                    self.m_pos[0] += d
                else:
                    self.m_pos[0] -= d
            elif self.m_direction == 2: # up
                direct = random.randint(1, 100)
                if direct > 1:
                    self.m_pos[1] -= d
                else:
                    self.m_pos[1] += d
            elif self.m_direction == 3: # down
                direct = random.randint(1, 100)
                if direct > 1:
                    self.m_pos[1] += d
                else:
                    self.m_pos[1] -= d

            # axis = random.randint(0, 1)
            # direct = random.randint(0, 1)
            # if x_avail and y_avail:
            #     if axis: # x
            #         if avail[0] and avail[1]:
            #             if direct: # [+]
            #                 self.m_pos[0] += d
            #             else:
            #                 self.m_pos[0] -= d
            #         elif avail[0]:
            #             self.m_pos[0] -= d
            #         else:
            #             self.m_pos[0] += d
            #     else:
            #         if avail[2] and avail[3]:
            #             if direct: # [+]
            #                 self.m_pos[1] += d
            #             else:
            #                 self.m_pos[1] -= d
            #         elif avail[2]:
            #             self.m_pos[1] -= d
            #         else:
            #             self.m_pos[1] += d
            # elif x_avail:
            #     if avail[0] and avail[1]:
            #         if direct: # [+]
            #             self.m_pos[0] += d
            #         else:
            #             self.m_pos[0] -= d
            #     elif avail[0]:
            #         self.m_pos[0] -= d
            #     else:
            #         self.m_pos[0] += d
            # elif y_avail:
            #     if avail[2] and avail[3]:
            #         if direct: # [+]
            #             self.m_pos[1] += d
            #         else:
            #             self.m_pos[1] -= d
            #     elif avail[2]:
            #         self.m_pos[1] -= d
            #     else:
            #         self.m_pos[1] += d
            chance -= 1


        if self.m_direction == 0:
            self.m_face = 0
        elif self.m_direction == 1:
            self.m_face = 1

        # print("[%f, %f] -> [%f, %f]" % (o_x, o_y, self.m_pos[0], self.m_pos[1]))
        # print("[%.2f, %.2f] -> [%.2f, %.2f]" % (o_x/100, o_y/100, self.m_pos[0]/100, self.m_pos[1]/100))
    def getpos(self, x, y):
        if x < 0:
            x = 0
        if y < 1:
            y = 1
        if x > G_WORLD_SIZE_W - 1:
            x = G_WORLD_SIZE_W - 1
        if y > G_WORLD_SIZE_H - 1:
            y = G_WORLD_SIZE_H - 1
        return [x, y]
    def blocks_ahead_of(self, maze, pos, direct):
        x = self.m_pos[0]
        y = self.m_pos[1]
        if pos == 0:
            if direct:
                x += self.m_speed[self.m_mode]/10
            else:
                x -= self.m_speed[self.m_mode]/10
        else:
            if direct:
                y += self.m_speed[self.m_mode]/10
            else:
                y -= self.m_speed[self.m_mode]/10

        ix, iy = int(x) % G_WORLD_SIZE_W, int(y) % G_WORLD_SIZE_H
        rx, ry = self.getpos(x, y)

        blocks = [maze[iy][ix]]
        if pos == 0: # X axis
            if direct == 0: # (-)
                blocks.append(maze[iy][ix - 1])
            else:
                blocks.append(maze[iy][ix + 1])
        else:
            if direct == 0: # (-)
                blocks.append(maze[iy - 1][ix])
            else:
                blocks.append(maze[iy + 1][ix])

        return blocks

class Pac_man(Ghost):
    def __init__(self, x, y):
        self.m_pos = [x, y]
        self.m_init_pos = [x, y]
        self.m_img = []
        self.m_img.append(pygame.image.load('images/pacman_o_yr.png'))
        self.m_img.append(pygame.image.load('images/pacman_c_yr.png'))
        self.m_img.append(pygame.image.load('images/pacman_o_y.png'))
        self.m_img.append(pygame.image.load('images/pacman_c_y.png'))
        self.m_mode = 1  # 0:strong 1:week 2:revival
        self.m_mode_tick = 0
        self.m_speed = [2, 4]
        self.m_direction = 1

class Map:
    def __init__(self, w, h, tile):
        self.w = w
        self.h = h
        self.tiles = []
        for row in tile:
            self.tiles.extend(row)

        # sets logging verbosity (on|off)
        self.verbose = False

    def __str__(self):
        s = "\n"
        i = 0
        for y in range(self.h):
            for x in range(self.w):
                s += self.tiles[i]
                i += 1
            s += "\n"
        return s

        # converts x,y to index

    def xy_to_i(self, x, y):
        return x + y * self.w

        # converts index to x,y

    def i_to_xy(self, i):
        return i % self.w, i / self.w

        # validates x,y

    def xy_valid(self, x, y):
        return x >= 0 and x < self.w and y >= 0 and y < self.h

        # gets tile at x,y or returns None if invalid

    def get_tile(self, x, y):
        if not self.xy_valid(x, y):
            return None
        return self.tiles[x + y * self.w]

        # adds a single wall tile at x,y

    def add_wall_tile(self, x, y):
        if self.xy_valid(x, y):
            self.tiles[x + y * self.w] = '|'

    def is_wall_block_filled(self, x, y):
        return all(self.get_tile(x + dx, y + dy) == '|' for dy in range(1, 3) for dx in range(1, 3))

        # adds a 2x2 block inside the 4x4 block at the given x,y coordinate

    def add_wall_block(self, x, y):
        self.add_wall_tile(x + 1, y + 1)
        self.add_wall_tile(x + 2, y + 1)
        self.add_wall_tile(x + 1, y + 2)
        self.add_wall_tile(x + 2, y + 2)

        # determines if a 2x2 block can fit inside the 4x4 block at the given x,y coordinate
        # (the whole 4x4 block must be empty)

    def can_new_block_fit(self, x, y):
        if not (self.xy_valid(x, y) and self.xy_valid(x + 3, y + 3)):
            return False
        for y0 in range(y, y + 4):
            for x0 in range(x, x + 4):
                if self.get_tile(x0, y0) != '.':
                    return False
        return True

        # create a list of valid starting positions

    def update_pos_list(self):
        self.pos_list = []
        for y in range(self.h):
            for x in range(self.w):
                if self.can_new_block_fit(x, y):
                    if self.w - 5 < x and self.h / 2 - 3 < y < self.h / 2 + 3:
                        continue
                    self.pos_list.append((x, y))
        # print(self.pos_list)
        # for pos in self.pos_list:
        #     print(pos)


        # A connection is a sort of dependency of one tile block on another.
        # If a valid starting position is against another wall, then add this tile
        # to other valid start positions' that intersect this one so that they fill
        # it when they are chosen.  This filling is a heuristic to eliminate gaps.

    def update_connections(self):
        self.connections = {}
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.pos_list:
                    if any(self.get_tile(x - 1, y + y0) == '|' for y0 in range(4)): self.add_connection(x, y, 1, 0)
                    if any(self.get_tile(x + 4, y + y0) == '|' for y0 in range(4)): self.add_connection(x, y, -1, 0)
                    if any(self.get_tile(x + x0, y - 1) == '|' for x0 in range(4)): self.add_connection(x, y, 0, 1)
                    if any(self.get_tile(x + x0, y + 4) == '|' for x0 in range(4)): self.add_connection(x, y, 0, -1)

        # the block at x,y is against a wall, so make intersecting blocks in the direction of
        # dx,dy fill the block at x,y if they are filled first.

    def add_connection(self, x, y, dx, dy):
        def connect(x0, y0):
            src = (x, y)
            dest = (x0, y0)
            if not dest in self.pos_list:
                return
            if dest in self.connections:
                self.connections[dest].append(src)
            else:
                self.connections[dest] = [src]

        if (x, y) in self.pos_list:
            connect(x + dx, y + dy)
            connect(x + 2 * dx, y + 2 * dy)
            if not (x - dy, y - dx) in self.pos_list: connect(x + dx - dy, y + dy - dx)
            if not (x + dy, y + dx) in self.pos_list: connect(x + dx + dy, y + dy + dx)
            if not (x + dx - dy, y + dy - dx) in self.pos_list: connect(x + 2 * dx - dy, y + 2 * dy - dx)
            if not (x + dx + dy, y + dy + dx) in self.pos_list: connect(x + 2 * dx + dy, y + 2 * dy + dx)

        # update the starting positions and dependencies

    def update(self):
        self.update_pos_list()
        self.update_connections()

        # expand a wall block at the given x,y
        # return number of tiles added

    def expand_wall(self, x, y):
        visited = []

        def expand(x, y):
            count = 0
            src = (x, y)
            if src in visited:
                return 0
            visited.append(src)
            if src in self.connections:
                for x0, y0 in self.connections[src]:
                    if not self.is_wall_block_filled(x0, y0):
                        count += 1
                        self.add_wall_block(x0, y0)
                    count += expand(x0, y0)
            return count

        return expand(x, y)

    def get_most_open_dir(self, x, y):
        dirs = ((0, -1), (0, 1), (1, 0), (-1, 0))
        max_dir = random.choice(dirs)
        max_len = 0
        for dx, dy in dirs:
            len = 0
            while (x + dx * len, y + dy * len) in self.pos_list:
                len += 1
            if len > max_len:
                max_dir = (dx, dy)
                max_len = len
        return max_dir

        # start a wall at block x,y

    def add_wall_obstacle(self, x=None, y=None, extend=False):
        self.update()
        if not self.pos_list:
            return False

        # choose random valid starting position if none provided
        if x is None or y is None:
            x, y = random.choice(self.pos_list)
        # print("Choosed %d %d" % (x, y))

        # add first block
        self.add_wall_block(x, y)

        # initialize verbose print lines
        first_lines = str(self).splitlines()
        grow_lines = [""] * (self.h + 2)
        extend_lines = [""] * (self.h + 2)

        # mandatory grow phase
        count = self.expand_wall(x, y)
        if count > 0:
            grow_lines = str(self).splitlines()

        # extend phase
        if extend:

            # desired maximum block size
            max_blocks = 4

            # 35% chance of forcing the block to turn
            # turn means the turn has been taken
            # turn_blocks is the number of blocks traveled before turning
            turn = False
            turn_blocks = max_blocks
            if random.random() <= 0.35:
                turn_blocks = 4
                max_blocks += turn_blocks

            # choose a random direction
            dx, dy = random.choice(((0, -1), (0, 1), (1, 0), (-1, 0)))
            orig_dir = (dx, dy)

            i = 0
            while count < max_blocks:
                x0 = x + dx * i
                y0 = y + dy * i
                # turn if we're past turning point or at a dead end
                if (not turn and count >= turn_blocks) or not (x0, y0) in self.pos_list:
                    turn = True
                    dx, dy = -dy, dx  # rotate
                    i = 1
                    # stop if we've come full circle
                    if orig_dir == (dx, dy):
                        break
                    else:
                        continue

                # add wall block and grow to fill gaps
                if not self.is_wall_block_filled(x0, y0):
                    self.add_wall_block(x0, y0)
                    count += 1 + self.expand_wall(x0, y0)
                i += 1
            extend_lines = str(self).splitlines()

        # print the map states after each phase for debugging
        if self.verbose:
            print("added block at ", x, y)
            for a, b, c in zip(first_lines, grow_lines, extend_lines):
                print(a, b, c)

        return True

class My_game:

    def __init__(self):
        self.m_title = "CG_PAC-MAN"

        self.m_score = 0
        self.m_remain = [0 ,0]
        self.m_life = 3
        self.m_tick = 0


        pygame.init()
        pygame.display.set_icon(pygame.image.load('images/logo.png'))
        pygame.display.set_caption(self.m_title)

        # self.m_screen_w = G_WORLD_SIZE_W * G_BLOCK_SIZE
        # self.m_screen_h = G_WORLD_SIZE_H * G_BLOCK_SIZE

        self.m_screen_w = 1000
        self.m_screen_h = 1000
        self.m_screen = pygame.display.set_mode((self.m_screen_w, self.m_screen_h))

        self.make_maze()
        self.m_screen = pygame.display.set_mode((G_WORLD_SIZE_W*2*G_BLOCK_SIZE, G_WORLD_SIZE_H*2*G_BLOCK_SIZE))

        self.m_pacman = Pac_man(1, G_WORLD_SIZE_H-1)

        for r in self.m_maze:
            for c in r:
                print(c, end=' ')
            print()


        # Set Ghosts
        self.m_ghosts = []
        for r in range(G_WORLD_SIZE_H // 2 - 1, G_WORLD_SIZE_H // 2 + 1):
            for c in range(G_WORLD_SIZE_W - 3, G_WORLD_SIZE_W):
                if self.m_maze[r + 1][c] == '@':
                    tmp = Ghost(c * 100, (r + 1) * 100)
                    self.m_ghosts.append(tmp)

                if self.m_maze[r + 1][2 * G_WORLD_SIZE_W - c - 1] == '@':
                    tmp = Ghost((2 * G_WORLD_SIZE_W - c - 1) * 100, (r + 1) * 100)
                    self.m_ghosts.append(tmp)
                self.m_maze[r + 1][c] = 'x'
                self.m_maze[r + 1][2 * G_WORLD_SIZE_W - c - 1] = 'x'
        self.m_maze[G_WORLD_SIZE_H//2-1][G_WORLD_SIZE_W-1] = 'x'
        self.m_maze[G_WORLD_SIZE_H//2-1][G_WORLD_SIZE_W] = 'x'



        # for r in self.m_maze:
        #     for c in r:
        #         print(c, end=' ')
        #     print()


        print("INIT DONE")

    def make_maze(self):
        # w = random.randint(12, 30)
        # h = random.randint(16, 30)
        w = G_WORLD_SIZE_W
        h = G_WORLD_SIZE_H
        # print(w, h)
        maze = [['.'] * w for i in range(h)]

        for r in range(h):
            for c in range(w):
                if r == 0 or c == 0 or r == h - 1:
                    maze[r][c] = '|'

        for r in range(h // 2 - 2, h // 2 + 2):
            for c in range(w - 4, w):
                maze[r][c] = '|'

        for r in range(h // 2 - 1, h // 2 + 1):
            for c in range(w - 3, w):
                maze[r][c] = '@'
        maze[h//2-2][w-1]='.'

        maze = Map(w, h, maze)

        while maze.add_wall_obstacle(extend=True):
            # for line in str(maze).splitlines():
            #     s = line
            #     print(s)
            pass

        # print(maze, type(maze))
        self.m_maze = []
        for line in str(maze).splitlines():
            tmp = []
            s = line
            for c in s:
                tmp.append(c)
            for c in s[::-1]:
                tmp.append(c)
            self.m_maze.append(tmp)

            # self.m_maze.append(s + s[::-1])
        # print(self.m_maze, type(self.m_maze))

        ori_maze = copy.deepcopy(self.m_maze)

        # Make power
        for r in range(len(ori_maze)):
            for c in range(len(ori_maze[r])):
                block = ori_maze[r][c]
                
                replace = 0
                if block == '.':
                    # ┐
                    if ori_maze[r-1][c] == '|' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '|':
                        replace = 2
                    # ┌
                    elif ori_maze[r-1][c] == '|' and ori_maze[r][c-1] == '|' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '.':
                        replace = 2
                    # ┘
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '|' and ori_maze[r][c+1] == '|':
                        replace = 2
                    # └
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '|' and ori_maze[r+1][c] == '|' and ori_maze[r][c+1] == '.':
                        replace = 2
                    # ├
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '|' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '.':
                        replace = 3
                    # ┬
                    elif ori_maze[r-1][c] == '|' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '.':
                        replace = 3
                    # ┤
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '|':
                        replace = 3
                    # ┴
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '|' and ori_maze[r][c+1] == '.':
                        replace = 3
                    # ┼
                    elif ori_maze[r-1][c] == '.' and ori_maze[r][c-1] == '.' and ori_maze[r+1][c] == '.' and ori_maze[r][c+1] == '.':
                        replace = 4
                # if replace > 2 and (self.m_maze[r-1][c] != '*' and self.m_maze[r][c-1] != '*' and self.m_maze[r+1][c] != '*' and self.m_maze[r][c+1] != '*')

                # if replace and (self.m_maze[r-1][c] != '*' and self.m_maze[r][c-1] != '*' and self.m_maze[r+1][c] != '*' and self.m_maze[r][c+1] != '*'):
                if replace:
                    self.m_maze[r][c] = '*'
                    # self.m_maze[r] = self.m_maze[r][:c] + '*' + self.m_maze[r][c+1:]

        # for r in self.m_maze:
        #     for c in r:
        #         print(c, end=' ')
        #     print()
        # print('================================')

        # only power at the corner
        # iterate through the rows and columns
        for row in range(len(self.m_maze)):
            for col in range(len(self.m_maze[row])):
                # if the current cell is a star
                if self.m_maze[row][col] == '*':
                    # check for contiguous stars to the left
                    left, right = col, col
                    while left >= 0 and self.m_maze[row][left] == '*':
                        left -= 1
                    left += 1
                    # check for contiguous stars to the right
                    while right < len(self.m_maze[row]) and self.m_maze[row][right] == '*':
                        right += 1
                    right -= 1
                    # check for contiguous stars above
                    up, down = row, row
                    while up >= 0 and self.m_maze[up][col] == '*':
                        up -= 1
                    up += 1
                    # check for contiguous stars below
                    while down < len(self.m_maze) and self.m_maze[down][col] == '*':
                        down += 1
                    down -= 1

                    # print("[%d, %d] u:%d d:%d l:%d r:%d" % (row, col, up, down, left, right))
                    # replace the non-corner stars with dots
                    for posy in range(up, down+1):
                        for posx in range(left, right+1):
                            self.m_maze[posy][posx] = '.'
                            # self.m_maze[posy] = self.m_maze[posy][:posx] + '.' + self.m_maze[posy][posx + 1:]

                    self.m_maze[up][left] = '*'
                    self.m_maze[up][right] = '*'
                    self.m_maze[down][left] = '*'
                    self.m_maze[down][right] = '*'
                    # self.m_maze[up] = self.m_maze[up][:left] + '*' + self.m_maze[up][left + 1:]
                    # self.m_maze[up] = self.m_maze[up][:right] + '*' + self.m_maze[up][right + 1:]
                    # self.m_maze[down] = self.m_maze[down][:left] + '*' + self.m_maze[down][left + 1:]
                    # self.m_maze[down] = self.m_maze[down][:right] + '*' + self.m_maze[down][right + 1:]

        # Set Ghost randomly
        while True:
            cnt_ghost = 0
            for r in range(h // 2 - 1, h // 2 + 1):
                for c in range(w - 3, w):
                    if random.randint(0, 1):
                        self.m_maze[r + 1][c] = ' '
                    else:
                        self.m_maze[r + 1][c] = '@'
                        cnt_ghost += 1
                    if random.randint(0, 1):
                        self.m_maze[r + 1][2 * w - c - 1] = ' '
                    else:
                        self.m_maze[r + 1][c] = '@'
                        cnt_ghost += 1
            # if cnt_ghost >= 4:
            if cnt_ghost == 1:
                break

        self.m_maze[G_WORLD_SIZE_H - 1][1] = ' '

        # Count point and power
        for r in self.m_maze:
            for c in r:
                if c == '.':
                    self.m_remain[0] += 1
                if c == '*':
                    self.m_remain[1] += 1

    def key_event(self, ke):
        x = self.m_pacman.m_pos[0]
        y = self.m_pacman.m_pos[1]
        d = self.m_pacman.m_direction
        if ke[pygame.K_LEFT]:
            x -= 1
            d = 0
        if ke[pygame.K_RIGHT]:
            x += 1
            d = 1
        if ke[pygame.K_UP]:
            y -= 1
        if ke[pygame.K_DOWN]:
            y += 1

        if self.m_maze[y][x] != '|':
            self.m_pacman.m_pos[0] = x
            self.m_pacman.m_pos[1] = y
            self.m_pacman.m_direction = d
            if self.m_maze[y][x] == '.':
                self.m_maze[y][x] = ' '
                self.m_score += 10
                self.m_remain[0] -= 1
            if self.m_maze[y][x] == '*':
                self.m_maze[y][x] = ' '
                self.m_score += 50
                self.m_remain[1] -= 1
                self.m_pacman.m_mode = 0
                self.m_pacman.m_mode_tick = G_FPS * 10

                for g in self.m_ghosts:
                    g.m_mode = 1

    def run(self):
        white = (255, 255, 255)
        black = (0, 0, 0)

        clock = pygame.time.Clock()
        while True:
            clock.tick(G_FPS)
            # print(clock)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.key_event(pygame.key.get_pressed())

            self.m_screen.fill(black)

            # Move position
            self.update()

            # Draw player & map
            self.draw()

            # 점수와 생명 수 텍스트 그리기
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(self.m_score), True, white)
            life_text = font.render("Life: " + str(self.m_life), True, white)

            # 텍스트를 화면의 원하는 위치에 추가
            self.m_screen.blit(score_text, (10, 5))
            screen_width = self.m_screen.get_width()
            text_width = life_text.get_width()
            text_x = screen_width - text_width - 10  # 우측 여백 10

            self.m_screen.blit(life_text, (text_x, 5 ))

            pygame.display.update()
            if sum(self.m_remain) == 2 or self.m_life < 0 or 1:
                break
        self.draw_game_over()

    def update(self):
        self.m_tick += 1
        self.m_tick %= G_FPS

        if self.m_pacman.m_mode != 1:
            self.m_pacman.m_mode_tick -= 1
            if self.m_pacman.m_mode_tick == 0:
                self.m_pacman.m_mode = 1


        # Move ghost
        for g in self.m_ghosts:
            g.move(self.m_maze)

            if g.m_out == 0 and (g.m_pos[0]/100 < G_WORLD_SIZE_W - 4 or g.m_pos[0]/100 > G_WORLD_SIZE_W + 3 or g.m_pos[1]/100 < G_WORLD_SIZE_H // 2 - 2 or g.m_pos[1]/100 > G_WORLD_SIZE_H // 2 + 2):
                g.m_out = 1

            # Check collision
            x1, y1 = map(lambda x : x / 100 * 32, g.m_pos)
            x2, y2 = map(lambda x : x * 32, self.m_pacman.m_pos)
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            print(x1/32, y1/32, x2/32, y2/32, distance)
            if distance < 2 * 16:
                if self.m_pacman.m_mode == 0: # pac-man strong -> ghost dead
                    g.m_mode = 2
                    g.m_mode_tick = G_FPS * 5
                    g.m_pos[0] = g.m_init_pos[0]
                    g.m_pos[1] = g.m_init_pos[1]
                elif self.m_pacman.m_mode == 1: # pac-man week -> revive
                    self.m_pacman.m_mode = 2
                    self.m_pacman.m_mode_tick = G_FPS * 5
                    self.m_score -= 100
                    self.m_life -= 1
                    self.m_pacman.m_pos[0] = self.m_pacman.m_init_pos[0]
                    self.m_pacman.m_pos[1] = self.m_pacman.m_init_pos[1]
    def draw_game_over(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        if sum(self.m_remain) == 2:
            print("WIN")
        else:
            self.m_screen.fill(black)
            font = pygame.font.Font(None, 72)
            output_text = font.render("GAME OVER", True, white)
            text_width = output_text.get_width()
            screen_w = self.m_screen.get_width()
            screen_h = self.m_screen.get_height()
            text_x = screen_w - text_width - 10  # 우측 여백 10

            self.m_screen.blit(output_text, (text_x, screen_h//2))

    def draw(self):
        char_to_image = {
            '.': 'images/dot.png',
            '|': 'images/wall.png',
            '*': 'images/power.png',
            # '@': 'images/ghost1.png',
            '@': '',
            't': 'images/pacman_c.png',
            ' ': '',
            'x': '',
        }

        # for row in self.m_maze:
        #     print(''.join(row))
        # for row in self.m_maze:
        #     for col in row:
        #         print(col, end=' ')
        #     print()

        # draw map
        for y, row in enumerate(self.m_maze):
            for x, block in enumerate(row):
                image = char_to_image[block]
                if image:
                    img = pygame.image.load(char_to_image[block])
                    self.m_screen.blit(img, (x*G_BLOCK_SIZE, y*G_BLOCK_SIZE))

        # draw pac_man
        pacman_img = self.m_pacman.m_img[self.m_pacman.m_direction * 2 + self.m_tick % 2]
        # pygame.image.load('images/pacman_or.png')

        if self.m_pacman.m_mode == 0:
            width = pacman_img.get_width()
            height = pacman_img.get_height()

            for y in range(height):
                for x in range(width):
                    color = pacman_img.get_at((x, y))
                    if color.r == 218 and color.g == 201 and color.b == 0:
                        new_color = pygame.Color(
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255)
                        )

                        pacman_img.set_at((x, y), new_color)

        self.m_screen.blit(pacman_img,
                           (self.m_pacman.m_pos[0]*G_BLOCK_SIZE,
                            self.m_pacman.m_pos[1]*G_BLOCK_SIZE)
                           )

        # draw ghosts
        for g in self.m_ghosts:
            ghost_img = g.m_img[g.m_mode * 2 + g.m_face]

            self.m_screen.blit(ghost_img,
                               (g.m_pos[0]/100*G_BLOCK_SIZE,
                                g.m_pos[1]/100*G_BLOCK_SIZE)
                               )




if __name__ == '__main__':
    while True:
        app = My_game()
        app.run()

import random

