import pygame, random
from pygame.math import Vector2 as vector
from helper import *
import numpy as np


class Pacman:
    def __init__(self, game, position):
        self.game = game
        self.starting_coordinate = [position.x, position.y]
        self.grid_coordinate = position
        self.pixel_coordinate = self.get_pixel_coordinate() 
        self.direction = vector(0, 0)
        self.lives = 3
        self.score = 0
        self.target = None
        self.minimax = Minimax(None, None)
        

    
#################### Get pixel co-rds ####################


    def get_pixel_coordinate(self):
        return vector((self.grid_coordinate[0] * SQUARE_WIDTH) + HALF_INDENT + SQUARE_WIDTH // 2, (self.grid_coordinate[1] * SQUARE_HEIGHT) + HALF_INDENT + SQUARE_HEIGHT // 2)


#################### UPDATE ####################


    def update_pacman(self):
        self.target = self.set_target()
        if self.target != self.grid_coordinate:
            self.pixel_coordinate += self.direction * 2
            if self.score % 15 == 0:
                random.shuffle(self.game.points)
            if self.is_time_to_move():
                self.move()

        self.grid_coordinate[0] = (self.pixel_coordinate[0]- INDENT + SQUARE_WIDTH//2)//SQUARE_WIDTH+1
        self.grid_coordinate[1] = (self.pixel_coordinate[1]- INDENT + SQUARE_HEIGHT//2)//SQUARE_HEIGHT+1
        if self.on_point():
            self.take_point()


#################### ... ####################


    def set_target(self):
        return self.game.points[0]

    def is_time_to_move(self):
        if int(self.pixel_coordinate.x + HALF_INDENT) % SQUARE_WIDTH == 0:
            if self.direction == vector(1, 0) or self.direction == vector(-1, 0) or self.direction == vector(0, 0):
                return True
        if int(self.pixel_coordinate.y + HALF_INDENT) % SQUARE_HEIGHT == 0:
            if self.direction == vector(0, 1) or self.direction == vector(0, -1) or self.direction == vector(0, 0):
                return True
        return False

    def move(self):
        self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_square = self.get_next_square(target)
        x = next_square[1] - self.grid_coordinate[0]
        y = next_square[0] - self.grid_coordinate[1]
        # xdir = next_square[0] - self.grid_coordinate[0]
        # ydir = next_square[1] - self.grid_coordinate[1]
        return vector(x, y)

    def get_next_square(self, target):
        map = [[0 for x in range(30)] for x in range(30)] #27/29
        for step in self.game.walls:
            if step[0] < 30 and step[1] < 30: #27/29
                map[int(step[1])][int(step[0])] = 1
        path = self.minimax.make_minimax(map, (int(self.grid_coordinate[1]), int(self.grid_coordinate[0])), (int(target[1]), int(target[0])))
        # path = self.Expect((int(self.grid_coordinate[0]), int(self.grid_coordinate[1])), (int(target[0]), int(target[1])))
        return path[1]

    def on_point(self): 
        if self.grid_coordinate in self.game.points:
            if self.direction == vector(1, 0) or self.direction == vector(-1, 0):
                return True
            if self.direction == vector(0, 1) or self.direction == vector(0, -1) or self.direction == vector(0, 0):
                return True
        return False

    def take_point(self):
        self.game.points.remove(self.grid_coordinate)
        self.score += 1
        if len(self.game.points) == 0 or self.score == 80:
            self.game.state = 'next'


#################### DISPLAY ####################


    def display_pacman(self):
        self.player_image = pygame.image.load('images/pacman.png')
        if self.direction == vector(0, -1):
            self.player_image = pygame.transform.rotate(self.player_image, 90)
        if self.direction == vector(0, 1):
            self.player_image = pygame.transform.rotate(self.player_image, -90)
        if self.direction == vector(-1, 0):
            self.player_image = pygame.transform.flip(self.player_image, 1, 0)
        self.player_image = pygame.transform.scale(self.player_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
        self.game.screen.blit(self.player_image, (int(self.pixel_coordinate.x - INDENT // 5),int(self.pixel_coordinate.y - INDENT // 5)))

    def display_lives(self):
        for x in range(self.lives):
            self.game.screen.blit(self.player_image, (30 + 20 * x, WINDOW_HEIGHT - 23))


















    ########## minimax ########## 



    def Expect(self, start, target):   
        grid = np.zeros((30, 28))
        queue = [start]
        path = []
        visited = []
        for step in self.app.lvlWalls:
            if step[0] < 28 and step[1] < 30:
                grid[int(step[1])][int(step[0])] = 1

        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)

            if current == target:

                break
            
            besides = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            for beside in besides:
                if beside[0] + current[0] >= 0 and beside[0] + current[0] < len(grid[0]):
                    if beside[1] + current[1] >= 0 and beside[1] + current[1] < len(grid):
                        nextCell = [beside[0] + current[0], beside[1] + current[1]]
                        if nextCell not in visited:
                            if grid[nextCell[1]][nextCell[0]] != 1:
                                queue.append(nextCell)
                                path.append([current, nextCell])

         
        bestPath = [target]
        while target != start:
            for step in path:
                if step[1] == target:
                    target = step[0]
                    bestPath.insert(0, step[0])
        
        return bestPath




class Minimax:
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def make_minimax(self, field, firstTarget, lastTarget):
        unchecked_coords = []
        checked_coords = []
        step = 0
        neighbours = ((0, -1), (1, 0), (0, 1), (-1, 0))
        step_limit = (len(field) // 2) ** 2
        first_top = Minimax(None, firstTarget)
        first_top.f = 0
        first_top.g = 0
        first_top.h = 0
        last_top = Minimax(None, lastTarget)
        last_top.f = 0
        last_top.g = 0
        last_top.h = 0
        unchecked_coords.append(first_top)

        while unchecked_coords:
            step += 1 # 
            curr_checked = unchecked_coords[0]
            curr_unchecked = 0

            for i, coord in enumerate(unchecked_coords):
                if coord.f < curr_checked.f:
                    curr_checked = coord
                    curr_unchecked = i 

            if step > step_limit:
                path = []
                curr_top = curr_checked
                
                while curr_top is not None:
                    path.append(curr_top.pos)
                    curr_top = curr_top.parent
                return path[::-1] 

            unchecked_coords.pop(curr_unchecked)
            checked_coords.append(curr_checked)

            if curr_checked == last_top:
                path = []
                curr_top = curr_checked
                while curr_top is not None:
                    path.append(curr_top.pos)
                    curr_top = curr_top.parent
                return path[::-1]

            childrens = []

            for neighbour in neighbours:
                top = (curr_checked.pos[0] + neighbour[0], curr_checked.pos[1] + neighbour[1])

                isInRange = [
                    top[0] < 0,
                    top[1] < 0,
                    top[0] > (len(field) - 1),
                    top[1] > (len(field[len(field) - 1]) - 1)
                ]

                if any(isInRange):
                    continue

                if field[top[0]][top[1]] != 0:
                    continue

                new_top = Minimax(curr_checked, top)

                childrens.append(new_top)

            for child in childrens:
                if len([node_child for node_child in checked_coords if node_child == child]) > 0:
                    continue

                child.g = curr_checked.g + 1
                child.h = ((child.pos[0] - last_top.pos[0]) ** 2) + ((child.pos[1] - last_top.pos[1]) ** 2)
                child.f = child.g + child.h

                if len([index_child for index_child in unchecked_coords if child == index_child and child.g > index_child.g]) > 0:
                    continue

                unchecked_coords.append(child)


    

