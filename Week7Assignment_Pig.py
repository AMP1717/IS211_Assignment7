import random
import argparse

class Die:
    def __init__(self, use_random_seed=False):
        if use_random_seed:
            random.seed()
        else:
            random.seed(0)
    
    def roll(self):
        input("\nPress Enter to roll the die!")
        num = random.randrange(1, 7)
        print(f"You rolled {num}!\n")
        return num
    
class Player:
    def __init__(self, player_number, die):
        self.num = player_number
        self.score = 0
        self.die = die
    
    def get_response(self):
        while True:
            response = input("Do you want to Roll or Hold (enter 'r' or 'h')? ").lower()
            if response in ["h", "hold"]:
                return "h"
            if response in ["r", "roll"]:
                return "r"
            print("Invalid input, try again.")


    def play(self, target):
        print(f"Player {self.num}, it is your turn, your score is {self.score}/{target}.")
        total = 0
        while True:
            roll = self.die.roll()

            if roll == 1:
                print(f"You rolled 1, your turn is over, your score is still {self.score}.")
                break

            total += roll
            if self.score + total >= target:
                self.score += total
                return
            
            print(f"This turn you got a total of {total}, which will increase your score from {self.score} to {self.score + total}")
            response = self.get_response()
            if response == 'h':
                self.score += total
                print(f"You added {total} to your score, your score is now {self.score}.")
                break
            else:
                continue
        input("Press Enter to end your turn.")




class Game:
    def __init__(self, number_of_players=2, use_random_seed=False, target=100):

        if number_of_players <= 1:
            raise ValueError("You need at least 2 players.")

        die = Die(use_random_seed)
        self.target = target

        self.players = [Player(i+1, die) for i in range(number_of_players)]
        self.current_player_index = 0

        

    def _get_current_player(self):
        return self.players[self.current_player_index]

    def _get_current_score(self):
        return self.players[self.current_player_index].score

    def _check_player_win(self):
        if self._get_current_score() >= self.target:
            return True
        return False

    def _move_player_index(self):
        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0

    def print_scores(self):
        print("\nCurrent scores:")
        for player in self.players:
            print(f"Player {player.num}: {player.score}/{self.target}")

        print()
        print(f"Next player is player {self.current_player_index + 1}.")
        print()

    def play(self):
        print(f"Welcome to pig game, try to hit target score of {self.target} first!")
        print(f"Rolling 1 ends your turn, rolling 2 - 5 gives you option to roll again or hold.")
        self.print_scores()
        while True:
            self._get_current_player().play(self.target)
            if self._check_player_win():
                print()
                print(f"Congratulations player {self.current_player_index + 1}, you reached the target of {self.target} and you have won!")
                break
            self._move_player_index()
            self.print_scores()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", help="Number of players", type=int, required=False, default=2)
    args = parser.parse_args()
    g = Game(use_random_seed=False, 
             target=100, 
             number_of_players=args.numPlayers)
    g.play()

main()