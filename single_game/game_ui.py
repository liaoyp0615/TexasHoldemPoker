import argparse
from game import Game

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--player_number', type=int, default=3)
    args.add_argument('--init_chips', type=int, default=300)
    args = args.parse_args()
    return args

def run(args):
    table_name = input("Please input the name of table: ")
    player_number = args.player_number
    int_chips = args.init_chips
    player_name = []
    for i in range(player_number):
        player_name.append(input("Please input the name of player %d: " % (i+1)))
    game = Game(table_name=table_name,
                player_number=player_number,
                player_name=player_name,
                init_chips=int_chips)
    game.start_game()
    pass

if __name__ == "__main__":
    args = parse_args()
    run(args)