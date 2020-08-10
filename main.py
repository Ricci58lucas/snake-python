import tkinter as tk
from PIL import Image, ImageTk
from random import randint

# TODO:
# set a starting menu with config setup options
# possible config options: window size, game speed, bg color?, font_size

# -- configuration -- #
BG_COLOR = "#577757"

FONT_SIZE = 12 # 11

# its half should always be divisible by SPRITE_SIZE
WIN_WIDTH = 200 # 200
WIN_HEIGHT = 200 # 200

MOVES_PER_SECOND = 5 # 5
GAME_SPEED = 1000 // MOVES_PER_SECOND

# amount of pixels snake advances when it moves
SPRITE_SIZE = 20

class Food():

    def __init__(self, snakePos):
        # set starting food position
        self.foodPos = self.pick_food_pos(snakePos)
        self.foodImg = self.load_image()

    def load_image(self):
        # check if assets exist
        try:
            return ImageTk.PhotoImage(Image.open("./assets/food.png"))
        except IOError as e:
            # print error and close window
            print(e)
            root.destroy()

    def pick_food_pos(self, snakePos):
        while True:   
            # set random y and x values within frame
            xPos = randint(1, (WIN_WIDTH-SPRITE_SIZE)/SPRITE_SIZE) * SPRITE_SIZE
            yPos = randint(1, (WIN_HEIGHT-SPRITE_SIZE)/SPRITE_SIZE) * SPRITE_SIZE
            foodPos = xPos, yPos

            if foodPos not in snakePos:
                return foodPos

    def get_food_pos(self):
        return self.foodPos

    def set_food_pos(self, value):
        self.foodPos = value

    def get_food_img(self):
        return self.foodImg

#--------------------------------------------------------------------------------------------------------------

class Snake():

    def __init__(self):
        # set starting head position at center of the frame
        self.snakePos = [(WIN_WIDTH/2, WIN_HEIGHT/2)]
        self.snakeImg = self.load_image()

    def load_image(self):
        # check if assets exist
        try:
            return ImageTk.PhotoImage(Image.open("./assets/snake.png"))
        except IOError as e:
            # print error and close window
            print(e)
            root.destroy()

    def check_collition(self):
        head_x_pos, head_y_pos = self.snakePos[0]
        return (
            head_x_pos in (0, WIN_WIDTH) or 
            head_y_pos in (0, WIN_HEIGHT) or 
            (head_x_pos, head_y_pos) in self.snakePos[1:]
        )
    
    def move(self, direction):
        new_head_pos = head_x_pos, head_y_pos = self.snakePos[0]

        if direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - SPRITE_SIZE)
        elif direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + SPRITE_SIZE)
        elif direction == "Left":
            new_head_pos = (head_x_pos - SPRITE_SIZE, head_y_pos)
        elif direction == "Right":
            new_head_pos = (head_x_pos + SPRITE_SIZE, head_y_pos)
            
        # update head and body positions in snakePos array
        self.snakePos = [new_head_pos] + self.snakePos[:-1]

    def eat(self):
        # duplicate the last element of the snake. This means that when it is removed (at move() method) there will be a copy there
        self.snakePos.append(self.snakePos[-1])

    def get_snake_pos(self):
        return self.snakePos

    def get_snake_img(self):
        return self.snakeImg

#--------------------------------------------------------------------------------------------------------------

class SnakeGame(tk.Canvas):

    def __init__(self):
        super().__init__(width = WIN_WIDTH, height = WIN_HEIGHT, background = BG_COLOR, highlightthickness = 0)

        self.snake = Snake()
        self.food = Food(self.snake.get_snake_pos())

        self.gameEnded = False
        self.score = 0
        self.currentDirection = ""

        # calls function self.key_press when any key is pressed
        self.bind_all("<Key>", self.key_press)

        # draw objects in canvas
        self.draw()

        # start update() loop
        self.after(GAME_SPEED, self.update)

    def draw(self):
        # draw starting head and food position
        self.create_image(*self.snake.get_snake_pos(), image = self.snake.get_snake_img(), tag = "snake")
        self.create_image(*self.food.get_food_pos(), image = self.food.get_food_img(), tag = "food")

        # draw border line
        self.create_rectangle(
            SPRITE_SIZE / 2, # left
            SPRITE_SIZE / 2, # top
            WIN_WIDTH - (SPRITE_SIZE / 2), # right
            WIN_HEIGHT - (SPRITE_SIZE / 2), # bottom
            outline = "#000000"
        )

    def update(self):
        if self.snake.check_collition():
            self.end_game()

        # check if head touched food
        if self.snake.get_snake_pos()[0] == self.food.get_food_pos():
            self.snake_ate()

        # update positions
        self.snake.move(self.currentDirection)
        # update drawing. move every image into its new position
        for element, position in zip(self.find_withtag("snake"), self.snake.get_snake_pos()):
            self.coords(element, position)

        self.after(GAME_SPEED, self.update)

    def snake_ate(self):
        self.snake.eat()
        # create image of last position of snake tail
        self.create_image(*self.snake.get_snake_pos()[-1], image = self.snake.get_snake_img(), tag="snake")
        
        self.food.set_food_pos(self.food.pick_food_pos(self.snake.get_snake_pos()))

        # move food image to new (random) position
        self.coords(self.find_withtag("food"), self.food.get_food_pos())

        self.score += 1

    def key_press(self, e):
        # get binded symbol of pressed key
        key_pressed = e.keysym

        allDirections = ("Up", "Down", "Left", "Right")
        allOpposites = ({"Up", "Down"}, {"Left", "Right"})

        if key_pressed in allDirections:
            new_direction = key_pressed
            # check if the direction is valid and if new direction is not opposite to current
            if {new_direction, self.currentDirection} not in allOpposites:
                self.currentDirection = new_direction
        elif key_pressed == "Escape":
            # close window
            root.destroy()
        elif key_pressed == "space" and self.gameEnded:
            # refresh game
            self.destroy()
            screen = SnakeGame()
            screen.pack()
            root.mainloop()

    def end_game(self):
        self.gameEnded = True

        self.delete(tk.ALL)
        self.create_text(
            WIN_WIDTH / 2,
            WIN_HEIGHT / 2,
            text = f"Game Over! Final Score: {self.score}\n Press space to start over",
            fill = "#000000",
            font = ("TkDefaultFont", FONT_SIZE)
        )


root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

# set the game
screen = SnakeGame()
screen.pack()

# loop over
root.mainloop()