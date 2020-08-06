import tkinter as tk
from PIL import Image, ImageTk
from random import randint

# -- frame, canvas and graphics configuration -- #
BG_COLOR = "#577757"

# its half should always be divisible by 20
WIN_WIDTH = 600
WIN_HEIGHT = 640

# -- game configuration -- #

MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND

# amount of pixels snake advances when it moves
# it should always be 20, as each image is 20x20 px
MOVE_INCREMENT = 20

# create our own canvas class (inheriting from tk.Canvas class)
class Snake(tk.Canvas):
    # load canvas pre-config (like a constructor)
    def __init__(self):
        super().__init__(width=WIN_WIDTH, height=WIN_HEIGHT, background=BG_COLOR, highlightthickness=0)

        # set starting snake_body and food positions
        self.snake_body_pos = [(WIN_WIDTH/2, WIN_HEIGHT/2)]
        self.food_pos = self.pick_new_food_pos()

        # set starting score and direction
        self.score = 0
        self.direction = "Right"

        # listen to keybord, execute self.key_press when key pressed
        self.bind_all("<Key>", self.key_press)

        # import and load snake_body and food images
        self.load_assets()
        # put objects (snake_body and food) in canvas
        self.draw()

        # wait [GAME_SPEED]ms and execute self.update
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
        # load snake and food images and "tag" every image object
        for x_pos, y_pos in self.snake_body_pos:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")

        self.create_image(*self.food_pos, image=self.food, tag="food")

        # draw border line
        self.create_rectangle(
            MOVE_INCREMENT/2, 
            MOVE_INCREMENT/2, 
            WIN_WIDTH-(MOVE_INCREMENT/2), 
            WIN_HEIGHT-(MOVE_INCREMENT/2), 
            outline="#000000"
        )

    def update(self):
        if self.check_collition():
            self.end_game()
            return

        # check if snake ate
        self.eat()

        # call move snake and then call perform_actions after 75ms
        self.move()
        self.after(GAME_SPEED, self.update)

    def check_collition(self):
        head_x_pos, head_y_pos = self.snake_body_pos[0]

        # return True if any is true
        return (
            # check if head touched borders
            head_x_pos in (0, WIN_WIDTH)
            or
            head_y_pos in (0, WIN_HEIGHT)
            or
            # check if head touched its body
            (head_x_pos, head_y_pos) in self.snake_body_pos[1:]
        )

    def eat(self):
        if self.snake_body_pos[0] == self.food_pos:
            # duplicate the last element of the snake (then remove it when self.move())
            self.snake_body_pos.append(self.snake_body_pos[-1])
            
            # create image of last position
            self.create_image(*self.snake_body_pos[-1], image=self.snake_body, tag="snake")

            # assing new random position to food
            self.food_pos = self.pick_new_food_pos()
            self.coords(self.find_withtag("food"), self.food_pos)

            # update score value
            self.score += 1

    def move(self):
        # obtain current head position
        head_x_pos, head_y_pos = self.snake_body_pos[0]
       
        # check direction and set movement
        if self.direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - MOVE_INCREMENT)
        elif self.direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + MOVE_INCREMENT)
        elif self.direction == "Left":
            new_head_pos = (head_x_pos - MOVE_INCREMENT, head_y_pos)
        elif self.direction == "Right":
            new_head_pos = (head_x_pos + MOVE_INCREMENT, head_y_pos)
        
        # update head and body positions in snake body array
        self.snake_body_pos = [new_head_pos] + self.snake_body_pos[:-1]

        # move every image object into its new position (update drawing)
        for element, position in zip(self.find_withtag("snake"), self.snake_body_pos):
            # moves "element" into "position"
            self.coords(element, position)

    def key_press(self, e):
        # get key press symbol ("Up", "Down", "Left", "Right")
        new_direction = e.keysym

        al_direction = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
            
        # check if the direction is valid and if new direction is nor opposite to current
        if (new_direction in al_direction) and {new_direction, self.direction} not in opposites:
                self.direction = new_direction

    def pick_new_food_pos(self):
        while True:
            # pick new random position
            x_pos = randint(1, (WIN_WIDTH-MOVE_INCREMENT)/MOVE_INCREMENT) * MOVE_INCREMENT
            y_pos = randint(1, (WIN_HEIGHT-MOVE_INCREMENT)/MOVE_INCREMENT) * MOVE_INCREMENT
            # set new position
            food_pos = (x_pos, y_pos)

            #check if position is inside snake
            if food_pos not in self.snake_body_pos:
                return food_pos

    def end_game(self):
        # erase every object in canvas and show final score
        self.delete(tk.ALL)
        self.create_text(
            WIN_WIDTH/2,
            WIN_HEIGHT/2, 
            text=f"Final Score: {self.score}",
            fill="#000000",
            font=("tkDefaultFont", 24)
        )

root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

# call our canvas class
screen = Snake()
screen.pack()

# start the loop
root.mainloop()