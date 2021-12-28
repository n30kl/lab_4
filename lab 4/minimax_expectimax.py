from pygame.locals import *
from ghost import *
from main import *


class Algorithm(object):
    def __init__(self, grid, ghosts, points, algo):
        self.grid = grid
        self.visited = []
        self.map = {}
        self.Graph()
        self.ghosts = ghosts
        self.points = points
        self.max = 100000000
        self.min = -100000000
        self.algo = algo


########  MINIMAX   ##########


    def minimax(self, depth, current, maximizing_player, alpha, beta, path):
        neighbour_len = list(set(self.map[current].keys()) - set(path))

        if depth == 0 or len(neighbour_len) == 0:
            return self.get_score(path)

        if maximizing_player:
            best = self.min
            best_path = path.copy()

            for gap in list(set(self.map[current].keys()) - set(path)):
                path.append(gap)
                val = self.minimax(depth - 1, gap, False, alpha, beta, path)
                best = max(best, val[0])

                if best == val[0]:
                    best_path.append(gap)

                path.remove(gap)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best, best_path
        else:
            best = self.max
            best_path = path.copy()

            for gap in list(set(self.map[current].keys()) - set(path)):
                path.append(gap)
                val = self.minimax(depth - 1, gap, True, alpha, beta, path)
                best = min(best, val[0])

                if best == val[0]:
                    best_path.append(gap)

                path.remove(gap)
                beta = min(beta, best)

                if beta <= alpha:
                    break
            return best, best_path

    def expectimax(self, depth, current, path, is_max):
        neighbour_count = list(set(self.map[current].keys()) - set(path))

        if depth == 0 or len(neighbour_count) == 0:
            return self.get_score(path)

        
        if is_max:
            best = self.min
            best_path = path.copy()

            for gap in self.map[current].keys():
                path.append(gap)
                val = self.expectimax(depth-1, gap, path, False)
                if best < val[0]:
                    best_path.append(gap)
                    best = val[0]
                path.remove(gap)
            return best, best_path
        else:
            best = 0
            best_path = path.copy()

            count = 0
            for gap in self.map[current].keys():
                path.append(gap)
                count += 1
                best += self.expectimax(depth - 1, gap, path, True)[0]
                path.remove(gap)
            if count != 0:
                best = best/count
            return best, best_path





    def get_score(self, path):
        priority = 0
        for gap in path:
            index = path.index(gap)
            if index + 1 < len(path):
                next = path[index + 1]
                for point in self.points:
                    if gap.position.x == next.position.x == point.position.x:
                        if point.position.y in range(gap.position.y, next.position.y) or \
                                point.position.y in range(next.position.y, gap.position.y):
                            priority += 10
                    if gap.position.y == next.position.y == point.position.y:
                        if point.position.x in range(gap.position.x, next.position.x) or \
                                point.position.x in range(next.position.x, gap.position.x):
                            priority += 10
            if gap in self.ghosts.get_road_blocks():
                priority -= 100
        return priority, path

    def get_path(self, path, start, goal):
        road = []
        current = goal
        while current != start:
            road.append(current)
            current = path[current]
        road.reverse()
        return road


    def re_main(self):
        pass