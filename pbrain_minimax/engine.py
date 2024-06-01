from backend import best_move


class Engine:
    def __init__(self):
        self.size   = ...
        self.board  = ...
        self.__turn = 0

    def protocol(self, *args):
        args = [str(i).lower() for i in args]
        print(f'MESSAGE {" ".join(args)}')
        match args[0]:
            case 'info':
                keyword = args[1]
                value   = args[2]
                print(f'MESSAGE [<-] {keyword} = {value}')
            case 'start':
                value = int(args[1])
                self.size = value
                self.board = [[' '] * value for _ in range(value)]
                print('OK')
            case 'begin':
                self.__turn += 1
                ay, ax = best_move(self.board, 'b')
                self.board[ay][ax] = 'b'
                return f'{ay},{ax}'
            case 'turn':
                self.__turn += 1
                color : str = lambda: 'w' if self.__turn % 2 == 0 else 'b'
                self.board[int(args[1].split(',')[0])][int(args[1].split(',')[1])] = color()
                ay, ax = best_move(self.board, color())
                self.__turn += 1
                self.board[ay][ax] = color()
                return f'{ay},{ax}'
            case 'end':
                exit()

    def interact(self):
        while True:
            inp = input().split()
            output = self.protocol(*inp)
            if output:
                print(output)


engine = Engine()
engine.interact()
