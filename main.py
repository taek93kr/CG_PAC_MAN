import random
import pygame
import sys
# https://shaunlebron.github.io/pacman-mazegen/



class Pac_man:
    def __init__(self):
        self.m_pos = [100, 100]
        self.m_point = 0
        self.m_life = 0
        self.m_img = pygame.image.load('images/pacman_o.png')

    def move(self):
        pass

class Ghost:
    def __init__(self):
        self.m_pos = [100, 100]

    def move(self):
        pass

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
                    if self.w - 5 > x and self.h / 2 - 3 < y < self.h / 2 + 3:
                        continue
                    self.pos_list.append((x, y))
        # print(self.pos_list)

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
    BLOCK_SIZE = 32

    def __init__(self):
        self.m_title = "CG_PAC-MAN"

        self.m_pacman = Pac_man()

        pygame.init()
        pygame.display.set_caption(self.m_title)

        self.m_world_size = random.randint(5, 10)
        # self.m_screen_w = self.m_world_size * self.BLOCK_SIZE
        # self.m_screen_h = self.m_world_size * self.BLOCK_SIZE

        self.m_screen_w = 1000
        self.m_screen_h = 1000
        self.m_screen = pygame.display.set_mode((self.m_screen_w, self.m_screen_h))

        self.make_maze()
        self.m_screen = pygame.display.set_mode((self.m_world_size*2*self.BLOCK_SIZE, self.m_world_size*2*self.BLOCK_SIZE))
        self.print_maze()

    def print_maze(self):
        char_to_image = {
            # '.': 'images/dot.png',
            '.': '',
            '|': 'images/wall.png',
            '*': 'images/power.png',
            '@': 'images/ghost1.png',
        }

        # for row in self.m_maze:
        #     print(''.join(row))
        # for row in self.m_maze:
        #     for col in row:
        #         print(col, end=' ')
        #     print()

        for y, row in enumerate(self.m_maze):
            for x, block in enumerate(row):
                image = char_to_image[block]
                if image:
                    img = pygame.image.load(char_to_image[block])
                    self.m_screen.blit(img, (x*self.BLOCK_SIZE, y*self.BLOCK_SIZE))
        self.m_screen.blit(self.m_pacman.m_img, (self.m_pacman.m_pos[0]*self.BLOCK_SIZE, self.m_pacman.m_pos[1]*self.BLOCK_SIZE))

    def make_maze(self):
        self.m_world_size = random.randint(15, 20)

        # w = random.randint(12, 30)
        # h = random.randint(16, 30)
        w = self.m_world_size
        h = self.m_world_size
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

        # for r in maze:
        #     print(r)

        maze = Map(w, h, maze)

        while maze.add_wall_obstacle(extend=True):
            pass

        self.m_maze = []
        # print(maze, type(maze))
        for line in str(maze).splitlines():
            s = line
            self.m_maze.append(s + s[::-1])

        # for r in self.m_maze:
        #     print(r)

    def key_event(self, ke):
        if ke[pygame.K_LEFT]:
            self.m_pacman.m_pos[0] -= 1
        if ke[pygame.K_RIGHT]:
            self.m_pacman.m_pos[0] += 1
        if ke[pygame.K_UP]:
            self.m_pacman.m_pos[1] -= 1
        if ke[pygame.K_DOWN]:
            self.m_pacman.m_pos[1] += 1

    def run(self):
        white = (255, 255, 255)
        black = (0, 0, 0)

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            # print(clock)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.key_event(pygame.key.get_pressed())

            # self.m_screen.fill(black)
            # pygame.draw.circle(self.m_screen, white, (self.m_pacman.m_pos[0], self.m_pacman.m_pos[1]), 20)
            pygame.display.update()

if __name__ == '__main__':
    app = My_game()
    app.run()

import random

