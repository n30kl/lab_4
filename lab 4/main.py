from pygame.math import Vector2 as vector
from helper import *
from pacman import *
from ghost import *
import sys, pygame


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_game_launched = True
        self.state = 'menu'
        self.walls = []
        self.points = []
        self.ghosts = []
        self.ghost_coordinates = []
        self.pacman_coordinate = None
        self.generate_level()
        self.Pacman = Pacman(self, vector(self.pacman_coordinate))
        self.create_ghosts()


    ########## Generate Level ##########


    def generate_level(self):
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        with open("maze.txt", 'r') as file:
            for y, line in enumerate(file):
                for x, sign in enumerate(line):
                    if sign == "w":
                        self.walls.append(vector(x, y))
                    elif sign == "p":
                        self.points.append(vector(x, y))
                    elif sign == "U":
                        self.pacman_coordinate = [x, y]
                    elif sign in ["1", "2", "3", "4"]:
                        self.ghost_coordinates.append([x, y])
        
        
    ########## Create Ghosts ##########

    def create_ghosts(self):
        for ghost, position in enumerate(self.ghost_coordinates):
            self.ghosts.append(Ghost(self, vector(position), ghost))


    ########## Reset Game ##########
    

    def reset_game(self):
        self.walls = []
        self.points = []        
        self.reset_pacman()
        self.reset_ghosts()
        self.generate_level() 
        self.state = "game"      

    def reset_pacman(self, is_reset = True):
        if is_reset:
            self.Pacman.lives = 3
        self.Pacman.grid_coordinate = vector(self.Pacman.starting_coordinate)
        self.Pacman.pixel_coordinate = self.Pacman.get_pixel_coordinate()
        self.Pacman.direction *= 0
        self.pacman_coordinate = None

    def reset_ghosts(self):
        self.ghost_coordinates = []
        for ghost in self.ghosts:
            ghost.grid_coordinate = vector(ghost.starting_coordinate)
            ghost.pixel_coordinate = ghost.get_pixel_coordinate()
            ghost.direction *= 0
            
  
    ########## Menu state ##########


    def menu_events(self):
        for event in pygame.event.get():
            self.close_by_esc(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'game'

    def menu_display(self):
        self.screen.fill(MENU_BACKGROUND_COLOUR)
        self.display_text(PLAY_AGAIN_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - INDENT], menu_TEXT_SIZE, MENU_TEXT_COLOUR, menu_FONT, centered = True)
        self.display_text(EXIT_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + INDENT], menu_TEXT_SIZE, MENU_TEXT_COLOUR, menu_FONT, centered = True)
        pygame.display.update()


    ########## Game state ##########


    def game_events(self):
        self.close_game()
                    
    def game_update(self):
        self.Pacman.update_pacman()
        for ghost in self.ghosts:
            ghost.update_ghost()
            if ghost.grid_coordinate == self.Pacman.grid_coordinate:
                self.delete_life()
                        
    def game_display(self):
        self.screen.fill(GAME_BACKGROUND_COLOUR)
        self.screen.blit(self.background, (HALF_INDENT, HALF_INDENT))
        self.display_text(f'SCORE: {self.Pacman.score}', self.screen, [280, 0], 18, SCORE_COLOUR, menu_FONT)
        self.display_lines()
        self.display_walls()
        self.display_points()
        self.Pacman.display_pacman()
        self.Pacman.display_lives()
        for ghost in self.ghosts:
            ghost.display_ghost()
        pygame.display.update()        


    ########## Result state ##########


    def result_events(self):
        for event in pygame.event.get():
            self.close_by_esc(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_game()

    def result_display(self):
        self.screen.fill(RESULT_BACKGROUND_COLOUR)
        self.display_text("You lose", self.screen, [WINDOW_WIDTH//2, 100],  52, RESULT_TEXT_COLOUR, "arial", True)
        self.display_text(PLAY_AGAIN_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2],  36, RESULT_COLOUR, "arial", True)
        self.display_text(EXIT_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5],  36, RESULT_COLOUR, "arial", True)
        pygame.display.update()


    ########## Next state ##########


    def next_events(self):
        for event in pygame.event.get():
            self.close_by_esc(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_game()

    def next_draw(self):
        self.screen.fill(RESULT_BACKGROUND_COLOUR)
        self.display_text("Level passed", self.screen, [WINDOW_WIDTH//2, 100],  52, RESULT_TEXT_COLOUR, "arial", True)
        self.display_text(PLAY_NEXT_LEVEL_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2],  36, RESULT_COLOUR, "arial", True)
        self.display_text(EXIT_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5],  36, RESULT_COLOUR, "arial", True)
        pygame.display.update()


#################### Delete Life ####################


    def delete_life(self):
        self.Pacman.lives -= 1
        if self.Pacman.lives == 0:
            self.Pacman.score = 0
            self.state = "result"          
        else:
            self.reset_pacman(False)
            self.reset_ghosts()


#################### Display ####################
        

    def display_lines(self):
        for x in range(X_LINE):
            pygame.draw.line(self.background, LINES_COLOUR, (x * SQUARE_WIDTH, 0), (x * SQUARE_WIDTH, WINDOW_HEIGHT))
        for y in range(Y_LINE):
            pygame.draw.line(self.background, LINES_COLOUR, (0, y * SQUARE_HEIGHT), (WINDOW_WIDTH, y * SQUARE_HEIGHT))

    def display_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.background, WALL_COLOUR, (wall.x * SQUARE_WIDTH, wall.y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

    def display_points(self):
        for point in self.points:
            pygame.draw.circle(self.screen, POINT_COLOUR, (int(point.x * SQUARE_WIDTH) + SQUARE_WIDTH // 2 + HALF_INDENT, int(point.y * SQUARE_HEIGHT) + SQUARE_HEIGHT // 2 + HALF_INDENT), 5)

    def display_text(self, words, screen, position, size, colour, fontName, centered = False):
        font = pygame.font.SysFont(fontName, size)
        text = font.render(words, False, colour)
        textSize = text.get_size()
        if centered:
            position[0] = position[0] - textSize[0] // 2
            position[1] = position[1] - textSize[1] // 2
        screen.blit(text, position)


#################### Close Game ####################


    def close_game(self):
        for event in pygame.event.get():
            self.close_by_esc(event)
    
    def close_by_esc(self, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_game_launched = False


#################### Launch Game ####################


    def run_game(self):
        while self.is_game_launched:
            if self.state == 'menu':
                self.menu_events()
                self.menu_display()
            elif self.state == 'game':
                self.game_events()
                self.game_update()
                self.game_display()
            elif self.state == 'result':
                self.result_events()
                self.result_display()
            elif self.state == 'next':
                self.next_events()
                self.next_draw()
            else:
                self.is_game_launched = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit() 


pygame.init()
game = Game().run_game()