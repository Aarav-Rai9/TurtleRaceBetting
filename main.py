import turtle
import random
import time
import tkinter as tk
from tkinter import messagebox

# Constants for track dimensions
TRACK_LENGTH = 700  # horizontal distance between start and finish
TRACK_WIDTH = 300   # total vertical span (radius = 150)
RADIUS = TRACK_WIDTH / 2  # 150
FINISH_LINE = -TRACK_LENGTH / 2 + TRACK_LENGTH  # 350

class TurtleRaceGUI:
    """
    A GUI-based turtle racing game with betting.
    During the race, a live status on the turtle screen shows what place
    the betted turtle is currently in.
    """
    def __init__(self, master):
        self.master = master
        master.title("Turtle Race Betting")
        self.tokens = 100
        self.odds = {"red": 1.5, "blue": 2.0, "green": 2.5,
                     "orange": 1.8, "purple": 3.0, "yellow": 1.2}
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
        """
        Draws an oval track with vertical start and finish lines.
        """
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.penup()
        start_x = -TRACK_LENGTH / 2  # -350

        # Draw outer oval: left semicircle, straight, right semicircle, straight
        drawer.goto(start_x, -RADIUS)
        drawer.pendown()
        drawer.circle(RADIUS, 180)      # left semicircle (bottom to top)
        drawer.forward(TRACK_LENGTH)      # top straight section
        drawer.circle(RADIUS, 180)      # right semicircle (top to bottom)
        drawer.forward(TRACK_LENGTH)      # bottom straight section
        drawer.penup()

        # Draw vertical start line at the left edge
        drawer.goto(start_x, -RADIUS)
        drawer.pendown()
        drawer.goto(start_x, RADIUS)
        drawer.penup()

        # Draw vertical finish line at the right edge
        finish_x = start_x + TRACK_LENGTH
        drawer.goto(finish_x, -RADIUS)
        drawer.pendown()
        drawer.goto(finish_x, RADIUS)
        drawer.penup()

    def setup_race(self):
        """
        Sets up the turtle screen and initializes racer turtles.
        Returns:
            screen: the turtle Screen object.
            racers: a list of turtle.Turtle objects for the race.
        """
        self.screen = turtle.Screen()
        self.screen.title("Turtle Race")
        # Use default window size
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)  # disable auto updates for performance

        # Draw the racing track
        self.draw_track()

        racers = []
        start_x = -TRACK_LENGTH / 2  # starting x-coordinate
        # Calculate lane centers for 6 lanes (evenly spaced)
        lane_spacing = TRACK_WIDTH / 6
        start_y_positions = [(-RADIUS) + lane_spacing/2 + i * lane_spacing for i in range(6)]

        for i, color in enumerate(self.colors):
            racer = turtle.Turtle(shape="turtle")
            racer.color(color)
            racer.penup()
            racer.speed(0)  # fastest drawing speed for racers
            racer.goto(start_x, start_y_positions[i])
            racers.append(racer)

        self.screen.update()  # update screen after drawing
        return self.screen, racers

    def race(self, racers, bet_color):
        """
        Runs the race until all turtles have finished.
        During the race, a status text is updated showing the current ranking
        of the betted turtle.
        Args:
            racers: list of turtle racers.
            bet_color: the color string of the turtle the user bet on.
        Returns:
            finish_order: list of turtles in the order they finished.
        """
        finish_order = []
        finished = set()

        # Create a status turtle for live update of betted turtle's rank.
        status_turtle = turtle.Turtle()
        status_turtle.hideturtle()
        status_turtle.penup()
        # Position the status text at the top center of the screen.
        status_turtle.goto(0, 260)

        while len(finish_order) < len(racers):
            for racer in racers:
                if racer not in finished:
                    racer.pendown()
                    racer.pensize(5)
                    racer.forward(random.randint(1, 10))
                    if racer.xcor() >= FINISH_LINE:
                        finish_order.append(racer)
                        finished.add(racer)
            # Compute current ranking based on x-coordinate (descending order)
            ranking = sorted(racers, key=lambda r: r.xcor(), reverse=True)
            # Find the current place of the betted turtle.
            for i, racer in enumerate(ranking, start=1):
                if racer.color()[0] == bet_color:
                    current_place = i
                    break
            # Update the status text
            status_turtle.clear()
            status_turtle.write(f"Your {bet_color} turtle is in {current_place} place",
                                align="center", font=("Arial", 16, "normal"))

            self.screen.update()
            time.sleep(0.05)
        return finish_order

    def start_race(self):
        """
        Handles bet validation, runs the race, updates tokens, and displays the result.
        Quits the game if no tokens remain.
        """
        # Check tokens
        if self.tokens <= 0:
            messagebox.showinfo("Game Over", "No tokens left. Game over!")
            self.quit_game()
            return

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

        screen, racers = self.setup_race()
        finish_order = self.race(racers, bet_color)

        # After race ends, clear the turtle screen.
        screen.clearscreen()

        # Determine final finishing position of the betted turtle.
        final_place = None
        for idx, racer in enumerate(finish_order, start=1):
            if racer.color()[0] == bet_color:
                final_place = idx
                break

        result_message = f"Your {bet_color} turtle finished in {final_place} place.\n"
        if final_place == 1:
            payout = int(bet_amount * self.odds[bet_color])
            self.tokens += payout
            result_message += f"Congratulations, you won {payout} tokens!"
        else:
            result_message += "Sorry, you lost the bet."

        self.update_tokens()
        messagebox.showinfo("Race Result", result_message)
        self.bet_entry.delete(0, tk.END)

        if self.tokens <= 0:
            messagebox.showinfo("Game Over", "No tokens left. Game over!")
            self.quit_game()

    def update_tokens(self):
        """
        Updates the token display in the GUI.
        """
        self.token_label.config(text=f"Tokens: {self.tokens}")

    def quit_game(self):
        """
        Quits the game.
        """
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TurtleRaceGUI(root)
    root.mainloop()
