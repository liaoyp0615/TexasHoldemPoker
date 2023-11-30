import os, sys
from player import Player
import datetime


class Game:
    
    def __init__(self, player_number=2, player_name=['play_A', 'play_B'], init_chips=300, **kwargs) -> None:
        self.test = kwargs.pop('test', False)
        self.verbose = kwargs.pop('verbose', False)
        self.table_name = kwargs.pop('table_name', 'table_test')
        self.table_file = f"../tables/{self.table_name}.txt"
        self.player_number = player_number
        self.init_chips = init_chips
        self.chips_on_table = 0
        # --- init players ---
        self.player = {}
        for i in range(self.player_number):
            self.player[i] = Player(name=player_name[i], chips=self.init_chips)
        
        # --- print the init info ---
        print("Welcome to the Texas Holdem Poker Game!")
        print(" The options you can use are:")
        print("   1. Start a new game: you need to set the player number, name, and chips")
        print("   2. Load a old game: you need to load the table file")
        print("   3. Show all players and their chips")
        print("   4. Show the rank of all players")
        print("   5. Bet for a player")
        print("   6. Get_chips for a player")
        print("   7. Set role for a player")
        print("   8. Quit the game")
        print("   9. Show the options")
        
        pass
    
    def set_player_name(self, player_id=0, name='default'):
        player_id -= 1
        self.player[player_id].set_name(name)
        self.add_log_to_table(log="Player '%s' is set to '%s'" % (self.player[player_id].name, name))
        pass

    def set_player_role(self, player_id=0, role=0):
        player_id -= 1
        self.player[player_id].set_role(role)
        self.add_log_to_table(log="Player '%s' is set to '%s'" % (self.player[player_id].name, role))
        pass

    def show_players(self):
        print(" In this game, there are %d players:")
        for i in range(self.player_number):
            self.player[i].show_self()
        pass


    def bet(self, player_id=0, chips=0, all_in=False):
        player_id -= 1
        if all_in:
            if self.player[player_id].chips>0:
                chips = self.player[player_id].chips
                print("You all in! You have %d chips!" % self.player[player_id].chips)
                self.add_log_to_table(log="You all in! You have %d chips!" % self.player[player_id].chips)
            else:
                print("You can not all in! You have %d chips!" % self.player[player_id].chips)
                self.add_log_to_table(log="You can not all in! You have %d chips!" % self.player[player_id].chips)
        self.player[player_id].bet(chips)
        self.chips_on_table += chips
        print("*Player '%s'  - %d chips   <%d>" % (self.player[player_id].name, chips, self.player[player_id].chips))
        self.add_log_to_table(log="*Player '%s'  - %d chips   <%d>" % (self.player[player_id].name, chips, self.player[player_id].chips))
        self.update_table()
        pass


    def get_chips(self, player_id=0, earn_chips=0):
        player_id -= 1
        self.player[player_id].get_chips(earn_chips)
        print("*Player '%s'  + %d chips   <%d>" % (self.player[player_id].name, earn_chips, self.player[player_id].chips))
        self.add_log_to_table(log="*Player '%s'  + %d chips   <%d>" % (self.player[player_id].name, earn_chips, self.player[player_id].chips))
        self.update_table()
        pass

    
    def get_chips_round(self, player_id=0):
        """ get chips for a player in a round """
        earn_chips = self.chips_on_table
        self.get_chips(player_id=player_id, earn_chips=earn_chips)
        self.chips_on_table = 0
        pass


    def get_rank(self):
        rank_player = []
        for i in range(self.player_number):
            rank_player.append(self.player[i])
        rank_player.sort(key=lambda x: x.chips, reverse=True)
        print("Ranking:")
        for i in range(self.player_number):
            print("  Rank %d: Player '%s' with %d chips" % (i+1, rank_player[i].name, rank_player[i].chips))
        self.add_log_to_table(log="Ranking:")
        for i in range(self.player_number):
            self.add_log_to_table(log="  Rank %d: Player '%s' with %d chips" % (i+1, rank_player[i].name, rank_player[i].chips))
        pass


    def new_table(self, **kwargs):
        """ Create a new table in the folder 'tables' """
        if not os.path.exists(self.table_file):
            with open(self.table_file, 'w') as f:
                f.write(" A new table is created at %s\n" % datetime.datetime.now())
                f.write(" The players are:\n")
                for i in range(self.player_number):
                    f.write("  Player %d : %s with %d chips\n" % (i+1, self.player[i].name, self.player[i].chips))
                f.write("\n")
        else:
            print("The table file '%s' already exists!" % self.table_file)
        pass


    def load_table(self, **kwargs):
        """ load a table from the folder 'tables' """
        if os.path.exists(self.table_file):
            player_number = 0
            player_name = []
            player_chips = []
            with open(self.table_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("  Player "):
                        player_number += 1
                        player_name.append(line.split(':')[1].split('with')[0].strip())
                        player_chips.append(int(line.split(':')[1].split('with')[1].strip().split(' ')[0]))
            print("The table file '%s' is loaded!" % self.table_file)
            print("  There are %d players:" % player_number)
            for i in range(player_number):
                print("    Player %d : %s with %d chips" % (i+1, player_name[i], player_chips[i]))
            self.player_number = player_number
            self.player = {}
            for i in range(self.player_number):
                self.player[i] = Player(name=player_name[i], chips=player_chips[i])
        else:
            print("The table file '%s' does not exist!" % self.table_file)
        pass
    

    def add_log_to_table(self, log="no message!", **kwargs):
        """ add log to the table """
        with open(self.table_file, 'a') as f:
            f.write(" log: %s  @ %s\n" % (log, datetime.datetime.now()))
        pass


    def update_table(self, **kwargs):
        """ update the player info in the table """
        with open(self.table_file, 'r') as f:
            lines = f.readlines()
            with open(self.table_file, 'w') as f:
                for line in lines:
                    if line.startswith(" The players are:"):
                        f.write(" The players are:\n")
                        for i in range(self.player_number):
                            f.write("  Player %d : %s with %d chips\n" % (i+1, self.player[i].name, self.player[i].chips))
                    elif line.startswith("  Player "):
                        pass
                    else:
                        f.write(line)
        pass

    def operate(self, opt=0, **kwargs):
        """ operate the game """
        if opt == 1:
            self.new_table()
        if opt == 2:
            self.load_table()
        if opt == 3:
            self.show_players()
        if opt == 4:
            self.get_rank()
        if opt == 5:
            player_id = int(input("Please input the player id: "))
            while player_id > self.player_number or player_id <= 0:
                print("The player id is out of range!")
                player_id = int(input("Please input the player id: "))
            
            chips = input("Please input the chips: ")
            if chips == 'allin':
                self.bet(player_id=player_id, chips=0, all_in=True)
            else:
                self.bet(player_id=player_id, chips=int(chips))
        if opt == 6:
            player_id = int(input("Please input the player id: "))
            while player_id > self.player_number or player_id <= 0:
                print("The player id is out of range!")
                player_id = int(input("Please input the player id: "))
            # earn_chips = int(input("Please input the earn chips: "))
            # self.get_chips(player_id=player_id, earn_chips=earn_chips)
            self.get_chips_round(player_id=player_id)
        if opt == 7:
            player_id = int(input("Please input the player id: "))
            while player_id > self.player_number or player_id <= 0:
                print("The player id is out of range!")
                player_id = int(input("Please input the player id: "))
            role = int(input("Please input the role: "))
            self.set_player_role(player_id=player_id, role=role)
        if opt == 8:
            print("Quit the game!")
            self.add_log_to_table(log="Quit the game!")
            sys.exit(0)
        if opt == 9:
            print(" The options you can use are:")
            print("   1. Start a new game: you need to set the player number, name, and chips")
            print("   2. Load a old game: you need to load the table file")
            print("   3. Show all players and their chips")
            print("   4. Show the rank of all players")
            print("   5. Bet for a player")
            print("   6. Get_chips for a player")
            print("   7. Set role for a player")
            print("   8. Quit the game")
            print("   9. Show the options")
        pass

    def start_game(self, **kwargs):
        """ start the game """
        while True:
            opt = int(input("\nPlease input the option: "))
            self.operate(opt=opt)
        pass

    def __call__(self, **kwargs):
        return "What an exciting game!"


if __name__ == "__main__":
    game = Game(player_number=3, player_name=['zhangsan', 'lisi', 'wangwu'], init_chips=300)
    game.start_game()