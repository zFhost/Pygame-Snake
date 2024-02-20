# PROJET NSI : SNAKE / ZASIR HAMALA ADAME ADAM

import pygame
import sys
import random


class Block: # représente une case
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos


class Food: # position de la nourriture dans la grille
    def __init__(self):
        x = random.randint(0, NB_COL - 1)
        y = random.randint(0, NB_ROW - 1)
        self.block = Block(x, y)

    def draw_food(self): # dessiner la nourriture
        rect = pygame.Rect(self.block.x * CELL_SIZE, self.block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (72, 212, 98), rect)


class Snake:  # représenter le snake
    def __init__(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"

    def draw_snake(self): # dessiner le snake
        for block in self.body:
            x_coord = block.x * CELL_SIZE
            y_coord = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (83, 177, 253), block_rect)

    def move_snake(self): # met à jour le bloc contenu dans le snake
        snake_block_count = len(self.body)
        old_head = self.body[snake_block_count - 1]

        if self.direction == "RIGHT":
            new_head = Block(old_head.x + 1, old_head.y)

        elif self.direction == "LEFT":
            new_head = Block(old_head.x - 1, old_head.y)

        elif self.direction == "TOP":
            new_head = Block(old_head.x, old_head.y - 1)

        else:
            new_head = Block(old_head.x, old_head.y + 1)

        self.body.append(new_head)

    def reset_snake(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.generate_food()

    def update(self): # met à jour les déplacements du snake
        self.snake.move_snake()
        self.check_head_on_food()
        self.game_over()

    def draw_game_element(self): # dessine les éléments du jeu
        self.food.draw_food()
        self.snake.draw_snake()

    def check_head_on_food(self): # vérifie si le snake "mange" la nourriture
        snake_length = len(self.snake.body)
        snake_head_block = self.snake.body[snake_length - 1]
        food_block = self.food.block
        if snake_head_block.x == food_block.x and snake_head_block.y == food_block.y:  # si oui on génère une nouvelle nourriture
            self.generate_food()
        else:
            self.snake.body.pop(0) # si non on supprime la queue du snake pour qu'il ne grandit pas à chaque déplacement

    def generate_food(self): # générer une nouvelle nourriture
        should_generate_food = True
        while should_generate_food:  # vérifie si la nourriture est généré sur le snake
            count = 0
            for block in self.snake.body:
                if block.x == self.food.block.x and block.y == self.food.block.y: # si non rien ne change la nourriture est bien générée
                    count += 1
            if count == 0:
                should_generate_food = False
            else: # si oui la nourriture est regénérée sans que le snake grandit
                self.food = Food()

    def game_over(self): # permet de savoir si le snake est sorti de la grille
        snake_length = len(self.snake.body)
        snake_head = self.snake.body[snake_length - 1]
        if (snake_head.x not in range(0, NB_COL)) or (snake_head.y not in range(0, NB_ROW)):
            self.snake.reset_snake()
        for block in self.snake.body[0:snake_length - 1]:
            if block.x == snake_head.x and block.y == snake_head.y:
                self.snake.reset_snake()

pygame.init()

NB_COL = 10 # Nombre de colonnes
NB_ROW = 15 # Nombre de lignes
CELL_SIZE = 40 # taille d'une case

screen = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE)) # Fenêtre de jeu
timer = pygame.time.Clock()

game_on = True
game = Game()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)


def show_grid(): # tracer la grille
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color('black'), rect, width=1)

while game_on: # boucle du jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN: # Permet à l'utilisateur de commander le snake
            if event.key == pygame.K_UP:
                if game.snake.direction != "DOWN": #On s'assure que le snake n'est pas déjà en train d'aller dans la direction voulue.
                    game.snake.direction = "TOP"
            if event.key == pygame.K_DOWN:
                if game.snake.direction != "TOP":
                    game.snake.direction = "DOWN"
            if event.key == pygame.K_LEFT:
                if game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"

    screen.fill(pygame.Color('white'))  # Couleur du fond
    show_grid()  # Afficher la grille
    game.draw_game_element() # Afficher les éléments du jeu
    pygame.display.update() # Met à jour le jeu 
    timer.tick(60) # Nombre de FPS
