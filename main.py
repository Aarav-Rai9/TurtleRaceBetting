import turtle
import random
import time


def setup_race():
    screen = turtle.Screen()
    screen.title("Turtle Race Betting")
    screen.setup(width=800, height=600)
    colors = ["red", "blue", "green", "orange", "purple", "yellow"]
    racers = []
    start_y = [-150, -100, -50, 0, 50, 100]
    for i in range(len(colors)):
        t = turtle.Turtle(shape="turtle")
        t.color(colors[i])
        t.penup()
        t.goto(-350, start_y[i])
        racers.append(t)
    return screen, racers


def race(racers):
    while True:
        for racer in racers:
            racer.forward(random.randint(1, 10))
            if racer.xcor() >= 350:
                return racer.color()[0]
        time.sleep(0.05)


def main():
    tokens = 100
    odds = {"red": 1.5, "blue": 2.0, "green": 2.5, "orange": 1.8, "purple": 3.0, "yellow": 1.2}

    while True:
        print("\nWelcome to Turtle Race Betting!")
        print(f"You have {tokens} tokens.")
        print("Turtles available and their odds:")
        for color, odd in odds.items():
            print(f"  {color}: {odd}")

        bet_color = input("Enter the colour you want to bet on: ").strip().lower()
        while bet_color not in odds:
            bet_color = input("Invalid colour. Choose from red, blue, green, orange, purple, yellow: ").strip().lower()

        bet_amount = int(input("Enter the number of tokens you want to bet: "))
        while bet_amount > tokens or bet_amount <= 0:
            bet_amount = int(input(f"Invalid bet amount. You have {tokens} tokens. Enter a valid bet: "))

        tokens -= bet_amount
        print(f"{bet_amount} tokens placed on {bet_color}. Tokens left: {tokens}")

        screen, racers = setup_race()
        print("The race is starting!")
        winner = race(racers)
        print(f"The winner is the {winner} turtle!")

        if bet_color == winner:
            payout = int(bet_amount * odds[winner])
            print(f"Congratulations! You won {payout} tokens!")
            tokens += payout
        else:
            print("Sorry, you lost the bet.")

        print(f"Tokens now: {tokens}")
        play_again = input("Play again? (y/n): ").strip().lower()
        # Clear the previous race drawing
        screen.clearscreen()
        if play_again != "y":
            print("Thanks for playing!")
            turtle.bye()  # Close the turtle graphics window
            break


if __name__ == "__main__":
    main()
