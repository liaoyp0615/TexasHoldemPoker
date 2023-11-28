import os, sys


class Player:
    
    def __init__(self, name='default', chips=300, special_role=0, **kwargs) -> None:
        self.name = name
        self.chips = chips
        self.sepcial_role = special_role  # 0/X: normal, 1: dealer, 2: small blind, 3: big blind
        self.test = kwargs.pop('test', False)
        self.verbose = kwargs.pop('verbose', False)
        pass

    def show_self(self, **kwargs):
        if self.sepcial_role == 1:
            role = 'dealer'
        elif self.sepcial_role == 2:
            role = 'small blind'
        elif self.sepcial_role == 3:
            role = 'big blind'
        else:
            role = 'normal'
        print("  My name is %s, role is '%s', and have %d chips" % (self.name, role, self.chips))
        pass
    
    def set_name(self, name):
        self.name = name
        pass

    def set_role(self, role):
        self.sepcial_role = role
        pass

    def bet(self, chips):
        self.chips -= chips
        pass

    def get_chips(self, earn_chips):
        self.chips += earn_chips
        pass

    def __call__(self, **kwargs):
        return "I am a smart player!"

if __name__ == "__main__":
    zhangsan = Player(name='zhangsan', chips=300)
    zhangsan.show_self()
    zhangsan.bet(100)
    zhangsan.show_self()
    zhangsan.get_chips(200)
    zhangsan.show_self()
    zhangsan.set_role(1)
    zhangsan.show_self()