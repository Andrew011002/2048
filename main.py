import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
import numpy as np
# from env2 import Env2048
import stable_baselines3 as sb3
import style
import sys
import os

path = os.path.abspath(os.path.dirname(__file__))
timestep = 2940
# model = sb3.PPO.load(f"Agents/Agent-{timestep}")

class Game(tk.Frame):

    def __init__(self, env, user=True, size=4):
        tk.Frame.__init__(self)
        self.grid()
        self.user = user
        self.env = env
        self.size = size
        self.main_grid = tk.Frame(self, bg=style.GRID_COLOR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.title = "2048" if self.user else "2048 AI"
        self.master.title(self.title)
        self.continue_update = True

        self.create_GUI() # GUI starts when Game() is called
        self.start_game()

        # default bindings
        self.master.bind("p", self.pause)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        ctk.set_appearance_mode("dark")

        # move input for user
        if self.user:
            self.master.bind("<Left>", self.left)
            self.master.bind("<Right>", self.right)
            self.master.bind("<Up>", self.up)
            self.master.bind("<Down>", self.down)
            self.master.bind("a", self.left)
            self.master.bind("d", self.right)
            self.master.bind("w", self.up)
            self.master.bind("s", self.down) 
        # Agent
        else:
            self.master.after(3000, self.update)

        self.mainloop() # get the infinite loop going
        

    # creates our grid of tiles
    def create_GUI(self):
        
        self.cells = [] # matrix to hold tiles

        # iterates rows and columns
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # creating a tile
                cell_frame = tk.Frame(self.main_grid, bg=style.EMPTY_CELL_COLOR, width=100, height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_num = tk.Label(self.main_grid, bg=style.EMPTY_CELL_COLOR)
                cell_num.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_num}
                row.append(cell_data) # add created tile to row     
            self.cells.append(row) # add populated row to matrix
        
        # Header labels

        # Creating and placing score label
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.25, y=40, anchor="center")
        tk.Label(score_frame, text="Score:", font=style.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=style.SCORE_LABEL_FONT)
        self.score_label.grid(row=0, column=1)

        # Creating and placing move label
        move_frame = tk.Frame(self)
        move_frame.place(relx=0.75, y=40, anchor="center")
        tk.Label(move_frame, text="Move:", font=style.SCORE_LABEL_FONT).grid(row=0)
        self.move_label = tk.Label(move_frame, text="0", font=style.SCORE_LABEL_FONT)
        self.move_label.grid(row=0, column=1)

    def start_game(self):

        # self.env = Env2048(self.size)
        # self.obs = self.env.reset()

        grid = self.env.get_grid()
        row, col = np.where(grid == 2)

        for row, col in zip(row, col):
            self.cells[row][col]["frame"].configure(bg=style.CELL_COLORS[2])
            self.cells[row][col]["number"].configure(bg=style.CELL_COLORS[2], fg=style.CELL_NUMBER_COLORS[2], font=style.CELL_NUMBER_FONTS[2], text="2")

    # updates the GUI when events occur
    def update(self):

        # # move agent until move is valid
        # if not self.user:
        #     temp = self.env.get_grid()
        #     while np.array_equal(temp, self.env.get_grid()):
        #         action = self.env.action_space.sample()
        #         self.obs, reward, done, truncation, info = self.env.step(action) # make move and get new observation (new state)

        for i in range(self.size):
            for j in range(self.size):
                cell_val = int(self.env.get_grid()[i][j])

                # tiles that are zero in the matrix
                if not cell_val:
                    self.cells[i][j]["frame"].configure(bg=style.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=style.EMPTY_CELL_COLOR, text="")

                # non-zero tiles in the matrix
                else:
                    self.cells[i][j]["frame"].configure(bg=style.CELL_COLORS[cell_val])
                    self.cells[i][j]["number"].configure(bg=style.CELL_COLORS[cell_val], fg=style.CELL_NUMBER_COLORS[cell_val], font=style.CELL_NUMBER_FONTS[cell_val], text=str(cell_val))
        
        # Updating score and move labels
        self.score_label.configure(text=str(int(self.env.grid.score)))
        self.move_label.configure(text=str(int(self.env.grid.moves)))

        if self.user:
            self.update_idletasks()
        else:
            self.game_over()
            if self.continue_update:
                self.master.after(500, self.update)

    def left(self, event):
        self.env.move("left")
        self.update()
        self.game_over() # check if was winning or losing move

    def right(self, event):
        self.env.move("right")
        self.update()
        self.game_over() # check if was winning or losing move

    def up(self, event):
        self.env.move("up")
        self.update()
        self.game_over() # check if was winning or losing move
    
    def down(self, event):
        self.env.move("down")
        self.update()
        self.game_over() # check if was winning or losing move

    def disable(self):

        self.master.unbind("p") # disable pause

        if self.user:
            self.master.unbind("w")
            self.master.unbind("a")
            self.master.unbind("s")
            self.master.unbind("d")
            self.master.unbind("<Left>")
            self.master.unbind("<Right>")
            self.master.unbind("<Up>")
            self.master.unbind("<Down>")
        else:
            self.continue_update = False

    def enable(self):

        self.master.bind("p", self.pause) 

        if self.user:

            self.master.bind("a", self.left)
            self.master.bind("d", self.right)
            self.master.bind("w", self.up)
            self.master.bind("s", self.down)
            self.master.bind("<Left>", self.left)
            self.master.bind("<Right>", self.right)
            self.master.bind("<Up>", self.up)
            self.master.bind("<Down>", self.down)
        else:
            self.continue_update = True
            self.update()

    def pause(self, event):

        self.pause_frame = tk.Frame(self.main_grid, bg=style.GRID_COLOR, bd=3, width=400, height=400)
        self.pause_frame.place(anchor="center", relx=0.5, rely=0.3)
        tk.Label(self.pause_frame, text="Paused", bg=style.EMPTY_CELL_COLOR, fg=style.CELL_NUMBER_COLORS[2], font=style.CELL_NUMBER_FONTS[4]).pack()

        self.resume_button = ctk.CTkButton(self, width=250, height=50, command=self.resume, text="Resume", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        self.resume_button.configure(text_color=style.CELL_NUMBER_COLORS[2], bg_color=style.EMPTY_CELL_COLOR, fg_color=style.CELL_COLORS[2], hover_color=style.CELL_COLORS[4])
        self.resume_button.place(anchor="center", relx=0.5, rely=0.6)

        self.quit_button = ctk.CTkButton(self, width=250, height=50, command=self.quit, text="Quit", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        self.quit_button.configure(text_color=style.CELL_NUMBER_COLORS[2], bg_color=style.EMPTY_CELL_COLOR, fg_color=style.CELL_COLORS[32], hover_color=style.CELL_COLORS[64])
        self.quit_button.place(anchor="center", relx=0.5, rely=0.75)

        self.disable()

    def resume(self):

        self.pause_frame.destroy()
        self.resume_button.destroy()
        self.quit_button.destroy()

        self.enable()

    def quit(self):
        self.disable()
        self.master.destroy()
        Menu()
        
    def game_over(self):

        status_code = self.env.game_over()

        if status_code == 2048:
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Won", bg=style.WINNER_BG, fg=style.GAME_OVER_FONT_COLOR, font=style.GAME_OVER_FONT).pack()
            self.disable() 
            
        elif status_code:
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Lost!", bg=style.LOSER_BG, fg=style.GAME_OVER_FONT_COLOR, font=style.GAME_OVER_FONT).pack()
            self.disable() 

class GridSelect(tk.Tk):

    def __init__(self, user=False):

        tk.Tk.__init__(self)
        self.title("Grids")
        self.geometry("420x420")
        self.configure(bg=style.EMPTY_CELL_COLOR)
        self.user = user # to init user play or agent play

        # 4x4 button that creates 4x4 grid
        _4x4 = ctk.CTkButton(self, width=250, height=50, command=self._4x4_, text="4x4", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        _4x4.configure(text_color=style.CELL_NUMBER_COLORS[2], fg_color=style.CELL_COLORS[2], hover_color=style.CELL_COLORS[4])
        _4x4.place(anchor="center", relx=0.5, rely=0.1)
        
        # 5x5 button that creates 5x5 grid
        _5x5 = ctk.CTkButton(self, width=250, height=50, command=self._5x5_, text="5x5", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        _5x5.configure(text_color=style.CELL_NUMBER_COLORS[16], fg_color=style.CELL_COLORS[8], hover_color=style.CELL_COLORS[16])
        _5x5.place(anchor="center", relx=0.5, rely=0.3)

        # 6x6 button that creates 6x6 grid
        _6x6 = ctk.CTkButton(self, width=250, height=50, command=self._6x6_, text="6x6", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        _6x6.configure(text_color=style.CELL_NUMBER_COLORS[2048], fg_color=style.CELL_COLORS[2048], hover_color=style.CELL_COLORS[1024])
        _6x6.place(anchor="center", relx=0.5, rely=0.5)

        # 7x7 button that creates 7x7 grid
        _7x7 = ctk.CTkButton(self, width=250, height=50, command=self._7x7_, text="7x7", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        _7x7.configure(text_color=style.CELL_NUMBER_COLORS[32], fg_color=style.CELL_COLORS[32], hover_color=style.CELL_COLORS[64])
        _7x7.place(anchor="center", relx=0.5, rely=0.7)

        # closes window and goes back to main Menu
        exit = ctk.CTkButton(self, width=250, height=50, command=self.quit, text="back", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        exit.configure(text_color=style.CELL_NUMBER_COLORS[2], fg_color=style.GRID_COLOR, hover_color=style.CELL_COLORS[64])
        exit.place(anchor="center", relx=0.5, rely=0.9)

        self.protocol("WM_DELETE_WINDOW", self.quit) # reload menu when X'ed out

        ctk.set_appearance_mode("dark") # set dark mode

        self.mainloop() # display and loop window

    # destroys window and calls the Menu back
    def quit(self):
        self.destroy()
        Menu()

    # starts 4x4 game based on the user passed in
    def _4x4_(self):
        self.destroy()
        Game(size=4, user=self.user)

    # starts 5x5 game based on the user passed in
    def _5x5_(self):
        self.destroy()
        Game(size=5, user=self.user)

    # starts 6x6 game based on the user passed in
    def _6x6_(self):
        self.destroy()
        Game(size=6, user=self.user)

    # starts 7x7 game based on the user passed in
    def _7x7_(self):
        self.destroy()
        Game(size=7, user=self.user)

# Main Menu
class Menu(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("2048 AI")
        self.geometry("420x420")
        self.configure(bg=style.EMPTY_CELL_COLOR)
        ctk.set_appearance_mode("dark")

        img = ImageTk.PhotoImage(Image.open(f"{path}/images/2048.png"))
        logo = tk.Label(self, bg=style.EMPTY_CELL_COLOR, image=img)
        logo.place(anchor="center", relx=0.5, rely=0.2)

        play_button = ctk.CTkButton(self, width=250, height=50, command=self.start_game, text="Start Game", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        play_button.configure(text_color=style.CELL_NUMBER_COLORS[2], fg_color=style.CELL_COLORS[2], hover_color=style.CELL_COLORS[4])
        play_button.place(anchor="center", relx=0.5, rely=0.45)

        rl_mode_button = ctk.CTkButton(self, width=250, height=50, command=self.load_model, text="RL Model", font=(style.CELL_NUMBER_FONTS[8][0], style.CELL_NUMBER_FONTS[8][1] - 25))
        rl_mode_button.configure(text_color=style.CELL_NUMBER_COLORS[8], fg_color=style.CELL_COLORS[8], hover_color=style.CELL_COLORS[16])
        rl_mode_button.place(anchor="center", relx=0.5, rely=0.65)

        quit_button = ctk.CTkButton(self, width=250, height=50, command=sys.exit, text="Quit", font=(style.CELL_NUMBER_FONTS[32][0], style.CELL_NUMBER_FONTS[32][1] - 25))
        quit_button.configure(text_color=style.CELL_NUMBER_COLORS[8], fg_color=style.CELL_COLORS[32], hover_color=style.CELL_COLORS[64])
        quit_button.place(anchor="center", relx=0.5, rely=0.85)
        ctk.set_appearance_mode("dark")

        self.mainloop() 

    def start_game(self):
        self.destroy()
        Game(user=True, size=4)  

    def load_model(self):
        self.destroy()
        Game(user=False, size=4)

if __name__ == "__main__":
    Menu()
