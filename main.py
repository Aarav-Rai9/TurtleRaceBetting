import turtle
import random
import time
import tkinter as tk
from tkinter import messagebox


class TurtleRaceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Turtle Race Betting")

        self.tokens = 100
        self.odds = {"red": 1.5, "blue": 2.0, "green": 2.5, "orange": 1.8, "purple": 3.0, "yellow": 1.2}
        self.colors = list(self.odds.keys())

        # Display tokens and odds
        self.token_label = tk.Label(master, text=f"Tokens: {self.tokens}")
        self.token_label.pack(pady=5)

        odds_text = "Odds:\n" + "\n".join(f"{color}: {odd}" for color, odd in self.odds.items())
        self.odds_label = tk.Label(master, text=odds_text)
        self.odds_label.pack(pady=5)

        # Betting widgets
        self.color_label = tk.Label(master, text="Select turtle color to bet on:")
        self.color_label.pack(pady=5)
        self.selected_color = tk.StringVar(master)
        self.selected_color.set(self.colors[0])
        self.color_menu = tk.OptionMenu(master, self.selected_color, *self.colors)
        self.color_menu.pack(pady=5)

        self.bet_label = tk.Label(master, text="Enter bet amount:")
        self.bet_label.pack(pady=5)
        self.bet_entry = tk.Entry(master)
        self.bet_entry.pack(pady=5)

        # Control buttons
        self.start_button = tk.Button(master, text="Start Race", command=self.start_race)
        self.start_button.pack(pady=5)
        self.quit_button = tk.Button(master, text="Quit", command=self.quit_game)
        self.quit_button.pack(pady=5)

    def draw_track(self):
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        # Define track dimensions (oval)
        track_length = 700  # horizontal distance between start and finish
        track_width = 300  # total vertical span; radius = 150
        radius = track_width / 2  # 150
        start_x = -track_length / 2  # -350

        # Draw the outer oval:
        drawer.penup()
        drawer.goto(start_x, -radius)
        drawer.pendown()
        # Draw left semicircle (from bottom to top)
        drawer.circle(radius, 180)
        # Draw top straight section
        drawer.forward(track_length)
        # Draw right semicircle (from top to bottom)
        drawer.circle(radius, 180)
        drawer.forward(track_length)
        drawer.penup()

        # Draw vertical start and finish lines:
        # Start line at left edge
        drawer.goto(start_x, -radius)
        drawer.pendown()
        drawer.goto(start_x, radius)
        drawer.penup()
        # Finish line at right edge
        finish_x = start_x + track_length
        drawer.goto(finish_x, -radius)
        drawer.pendown()
        drawer.goto(finish_x, radius)
        drawer.penup()

    def setup_race(self):
        self.screen = turtle.Screen()
        self.screen.title("Turtle Race")
        self.screen.setup(width=800, height=600)
        # Draw the horse racing track background
        self.draw_track()

        racers = []
        track_length = 700
        track_width = 300
        radius = track_width / 2  # 150
        start_x = -track_length / 2  # -350
        # Calculate lane centers for 6 lanes (evenly spaced within the track)
        lane_spacing = track_width / 6  # 50
        start_y_positions = [(-radius) + lane_spacing / 2 + i * lane_spacing for i in range(6)]

        for i, color in enumerate(self.colors):
            racer = turtle.Turtle(shape="turtle")
            racer.color(color)
            racer.penup()
            racer.goto(start_x, start_y_positions[i])
            racers.append(racer)
        return self.screen, racers

    def race(self, racers):
        finish_line = 350  # since start_x = -350 and track_length = 700
        while True:
            for racer in racers:
                racer.forward(random.randint(1, 10))
                if racer.xcor() >= finish_line:
                    return racer.color()[0]
            time.sleep(0.05)

    def start_race(self):
        try:
            bet_amount = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for bet amount.")
            return

        if bet_amount <= 0 or bet_amount > self.tokens:
            messagebox.showerror("Invalid bet", f"Bet must be between 1 and {self.tokens}.")
            return

        bet_color = self.selected_color.get()
        self.tokens -= bet_amount
        self.update_tokens()

        # Run the race using Turtle graphics with the new track drawing
        screen, racers = self.setup_race()
        winner = self.race(racers)
        # Instead of closing, clear for the next race
        screen.clearscreen()

        result_message = f"The winner is the {winner} turtle!\n"
        if bet_color == winner:
            payout = int(bet_amount * self.odds[winner])
            self.tokens += payout
            result_message += f"Congratulations, you won {payout} tokens!"
        else:
            result_message += "Sorry, you lost the bet."

        self.update_tokens()
        messagebox.showinfo("Race Result", result_message)
        self.bet_entry.delete(0, tk.END)

    def update_tokens(self):
        self.token_label.config(text=f"Tokens: {self.tokens}")

    def quit_game(self):
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TurtleRaceGUI(root)
    root.mainloop()
