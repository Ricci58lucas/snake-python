import tkinter as tk
from PIL import Image, ImageTk
from random import randint

# -- graphics configuration -- #
BG_COLOR = "#577757"

# its half should always be divisible by 20
WIN_WIDTH = 600
WIN_HEIGHT = 640

# -- game mechanics configuration -- #

MOVES_PER_SECOND = 17
GAME_SPEED = 1000 // MOVES_PER_SECOND

# amount of pixels snake advances when it moves
# should always be 20, as each image is 20x20 px
MOVE_INCREMENT = 20

# create our own canvas class (inheriting from tk.Canvas class)
class SnakeGame(tk.Canvas):
    def __init__(self):
        super().__init__(width=WIN_WIDTH, height=WIN_HEIGHT, background=BG_COLOR, highlightthickness=0)

        self.game_ended = False

        # set starting snake_body and food positions
        self.snake_body_pos = [(WIN_WIDTH/2, WIN_HEIGHT/2)]
        self.food_pos = self.pick_new_food_pos()

        self.score = 0

        # all posible directions and all posible opposites
        self.all_direction = ("Up", "Down", "Left", "Right")
        self.opposites = ({"Up", "Down"}, {"Left", "Right"})
        
        self.direction = ""

        # call function self.key_press when any key is pressed
        self.bind_all("<Key>", self.key_press)

        # import and load snake_body and food images
        self.load_assets()
        # draw objects in canvas
        self.draw()

        # start loop
        self.after(GAME_SPEED, self.update)

    def load_assets(self):
        # check if assets exist
        try:
            # get images from assets
            self.snake_body = ImageTk.PhotoImage(Image.open("./assets/snake.png"))
            self.food = ImageTk.PhotoImage(Image.open("./assets/food.png"))
        except IOError as e:
            # print error and close window
            print(e)
            root.destroy()

    def draw(self):
        # draw snake and food images and nametag them
        for x_pos, y_pos in self.snake_body_pos:
            self.create_image(x_pos, y_pos, image = self.snake_body, tag = "snake")

        self.create_image(*self.food_pos, image = self.food, tag = "food")

        # draw border line
        self.create_rectangle(
            MOVE_INCREMENT/2, 
            MOVE_INCREMENT/2, 
            WIN_WIDTH - (MOVE_INCREMENT/2), 
            WIN_HEIGHT - (MOVE_INCREMENT/2), 
            outline = "#000000"
        )

    def update(self):
        if self.check_collition():
            self.end_game()

        if self.snake_body_pos[0] == self.food_pos:
            self.eat()

        if self.direction in self.all_direction:
            self.move()

        self.after(GAME_SPEED, self.update)

    def check_collition(self):
        head_x_pos, head_y_pos = self.snake_body_pos[0]
        return (
            head_x_pos in (0, WIN_WIDTH) or 
            head_y_pos in (0, WIN_HEIGHT) or 
            (head_x_pos, head_y_pos) in self.snake_body_pos[1:]
        )

    def eat(self):
        # duplicate the last element of the snake (then remove it when self.move())
        self.snake_body_pos.append(self.snake_body_pos[-1])
                
        # create image of last position
        self.create_image(*self.snake_body_pos[-1], image=self.snake_body, tag="snake")

        self.food_pos = self.pick_new_food_pos()
        self.coords(self.find_withtag("food"), self.food_pos)

        self.score += 1

    def key_press(self, e):
        # get binded symbol of pressed key
        key_pressed = e.keysym

        if key_pressed in self.all_direction:
            new_direction = key_pressed

            # check if the direction is valid and if new direction is not opposite to current
            if {new_direction, self.direction} not in self.opposites:
                self.direction = new_direction
        elif key_pressed == "Escape":
            # close window
            root.destroy()
        elif key_pressed == "space" and self.game_ended:
            # refresh game
            self.destroy()
            screen = SnakeGame()
            screen.pack()
            root.mainloop()
      
    def move(self):
        head_x_pos, head_y_pos = self.snake_body_pos[0]
       
        if self.direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - MOVE_INCREMENT)
        elif self.direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + MOVE_INCREMENT)
        elif self.direction == "Left":
            new_head_pos = (head_x_pos - MOVE_INCREMENT, head_y_pos)
        elif self.direction == "Right":
            new_head_pos = (head_x_pos + MOVE_INCREMENT, head_y_pos)
        
        # update head and body positions in snake_body array
        self.snake_body_pos = [new_head_pos] + self.snake_body_pos[:-1]

        # update drawing. move every image object into its new position
        for element, position in zip(self.find_withtag("snake"), self.snake_body_pos):
            self.coords(element, position)

    def pick_new_food_pos(self):
        while True:
            x_pos = randint(1, (WIN_WIDTH-MOVE_INCREMENT)/MOVE_INCREMENT) * MOVE_INCREMENT
            y_pos = randint(1, (WIN_HEIGHT-MOVE_INCREMENT)/MOVE_INCREMENT) * MOVE_INCREMENT
            food_pos = (x_pos, y_pos)

            # prevent food from spawning inside snake
            if food_pos not in self.snake_body_pos:
                return food_pos

    def end_game(self):
        self.game_ended = True

        # deletes canvas content
        self.delete(tk.ALL)
        self.create_text(
            WIN_WIDTH/2,
            WIN_HEIGHT/2,
            text = f"Game Over! Final Score: {self.score}\nPress space to Start Over",
            fill = "#000000",
            font = ("TkDefaultFont", 24)
        )
      
root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

# call our canvas class
screen = SnakeGame()
screen.pack()

# start the loop
root.mainloop()