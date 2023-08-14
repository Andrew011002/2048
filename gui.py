import os
import sys
import style
import numpy as np
import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from env2 import Env2048

path = os.path.abspath(os.path.dirname(__file__))

class Game(tk.Frame):

    def __init__(self, user=True, size=4, menu=False):
        tk.Frame.__init__(self)
        self.grid()
        self.user = user
        self.size = size
        self.menu = menu
        self.main_grid = tk.Frame(self, bg=style.GRID_COLOR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.title = "2048" if self.user else "2048 AI"
        self.master.title(self.title)
        self.paused = False

        self.create_grid() 
        self.setup_grid()
        self.start_game()
        self.mainloop()

    def create_grid(self):
        
        self.cells = [] 

        for i in range(self.size):
            row = []
            for j in range(self.size):

                cell_frame = tk.Frame(self.main_grid, bg=style.EMPTY_CELL_COLOR, width=100, height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_num = tk.Label(self.main_grid, bg=style.EMPTY_CELL_COLOR)
                cell_num.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_num}
                row.append(cell_data) 

            self.cells.append(row) 
        
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.25, y=40, anchor="center")
        tk.Label(score_frame, text="Score:", font=style.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=style.SCORE_LABEL_FONT)
        self.score_label.grid(row=0, column=1)

        move_frame = tk.Frame(self)
        move_frame.place(relx=0.75, y=40, anchor="center")
        tk.Label(move_frame, text="Move:", font=style.SCORE_LABEL_FONT).grid(row=0)
        self.move_label = tk.Label(move_frame, text="0", font=style.SCORE_LABEL_FONT)
        self.move_label.grid(row=0, column=1)

    def start_game(self):
        
        self.env = Env2048(self.size)
        self.obs = self.env.reset()

        grid = self.env.numpy()
        row, col = np.where(grid == 2)

        for row, col in zip(row, col):
            self.cells[row][col]["frame"].configure(bg=style.CELL_COLORS[2])
            self.cells[row][col]["number"].configure(bg=style.CELL_COLORS[2], fg=style.CELL_NUMBER_COLORS[2], 
                                                     font=style.CELL_NUMBER_FONTS[2], text="2")
    def update(self):

        if self.paused:
            return None
        
        if not self.user:

            self.run_model()

        grid = self.env.numpy()

        for i in range(self.size):
            for j in range(self.size):
                cell_val = int(grid[i][j])

                if not cell_val:

                    self.cells[i][j]["frame"].configure(bg=style.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=style.EMPTY_CELL_COLOR, text="")

                else:
                    self.cells[i][j]["frame"].configure(bg=style.CELL_COLORS[cell_val])
                    self.cells[i][j]["number"].configure(bg=style.CELL_COLORS[cell_val], fg=style.CELL_NUMBER_COLORS[cell_val], 
                                                         font=style.CELL_NUMBER_FONTS[cell_val], text=str(cell_val))        
                    
        self.score_label.configure(text=str(int(self.env.score())))
        self.move_label.configure(text=str(int(self.env.moves())))

        self.game_over()

        self.update_idletasks()
        if not self.user:
            self.master.after(250, self.update)

    def left(self, event):

        if not self.paused:
            self.env.move("left")
            self.update()

    def right(self, event):

        if not self.paused:
            self.env.move("right")
            self.update()

    def up(self, event):

        if not self.paused:
            self.env.move("up")
            self.update()
    
    def down(self, event):

        if not self.paused:
            self.env.move("down")
            self.update()

    def run_model(self):
        action = self.env.action_space.sample()
        obs, reward, done, truncated, info = self.env.step(action)

    def pause(self, event):

        self.paused = not self.paused

        if self.paused:
            self.setup_pause()
        else:
            self.resume()

    def setup_pause(self):

        self.pause_frame = tk.Frame(self.main_grid, bg=style.GRID_COLOR, bd=3, width=400, height=400)
        self.pause_frame.place(anchor="center", relx=0.5, rely=0.3)
        tk.Label(self.pause_frame, text="Paused", bg=style.EMPTY_CELL_COLOR, fg=style.CELL_NUMBER_COLORS[2], font=style.CELL_NUMBER_FONTS[4]).pack()

        self.resume_button = ctk.CTkButton(self, width=250, height=50, command=self.resume, text="Resume", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        self.resume_button.configure(text_color=style.CELL_NUMBER_COLORS[2], bg_color=style.EMPTY_CELL_COLOR, fg_color=style.CELL_COLORS[2], hover_color=style.CELL_COLORS[4])
        self.resume_button.place(anchor="center", relx=0.5, rely=0.6)

        self.quit_button = ctk.CTkButton(self, width=250, height=50, command=self.quit, text="Quit", font=(style.CELL_NUMBER_FONTS[2][0], style.CELL_NUMBER_FONTS[2][1] - 25))
        self.quit_button.configure(text_color=style.CELL_NUMBER_COLORS[2], bg_color=style.EMPTY_CELL_COLOR, fg_color=style.CELL_COLORS[32], hover_color=style.CELL_COLORS[64])
        self.quit_button.place(anchor="center", relx=0.5, rely=0.75)

    def resume(self):

        self.paused = False
        self.pause_frame.destroy()
        self.resume_button.destroy()
        self.quit_button.destroy()
        self.update()

    def quit(self):

        self.master.destroy()

        if self.menu:
            Menu()
        
    def game_over(self):

        status_code = self.env.game_over()

        if status_code == 2048:
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Won", bg=style.WINNER_BG, fg=style.GAME_OVER_FONT_COLOR, font=style.GAME_OVER_FONT).pack()
            self.master.unbind("p")
            
        elif status_code:
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Lost!", bg=style.LOSER_BG, fg=style.GAME_OVER_FONT_COLOR, font=style.GAME_OVER_FONT).pack()
            self.master.unbind("p")

    def setup_grid(self):

        self.master.bind("p", self.pause)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        ctk.set_appearance_mode("dark")

        if self.user:
            self.master.bind("<Left>", self.left)
            self.master.bind("<Right>", self.right)
            self.master.bind("<Up>", self.up)
            self.master.bind("<Down>", self.down)
            self.master.bind("a", self.left)
            self.master.bind("d", self.right)
            self.master.bind("w", self.up)
            self.master.bind("s", self.down) 
        else:
            self.master.after(1000, self.update)

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

        self.mainloop() 

    def start_game(self):
        self.destroy()
        Game(user=True, size=4, menu=True)  

    def load_model(self):
        self.destroy()
        Game(user=False, size=4, menu=True)

def main():
    menu = Menu()

if __name__ == "__main__":
    main()