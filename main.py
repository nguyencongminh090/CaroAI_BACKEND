import PyGomo
import numpy
from time import perf_counter as clock
from pbrain_minimax import Engine


ENGINE     = PyGomo.Engine(r'pbrain_embryo.exe')
PROTOCOL   = PyGomo.GomocupProtocol()
CONTROLLER = PyGomo.Controller()

CONTROLLER.setProtocol(PROTOCOL)
CONTROLLER.setEngine(ENGINE)

BOARD = ...
TIME  = ...

def getMoveFromBoard(board):
    global BOARD
    nBoard = numpy.array(board)
    # Check if board is empty
    if BOARD is Ellipsis:
        boardSize = nBoard.shape
        BOARD = numpy.array([[' '] * boardSize[0] for _ in range(boardSize[1])])
    
    coordinates = numpy.where(board != BOARD)
    BOARD = nBoard

    # [1][0] is X coord
    return None if not coordinates[1].any() and not coordinates[0].any() else f'{coordinates[1][0]},{coordinates[0][0]}'


def loadEngine(enginePath):
    global ENGINE, CONTROLLER, PROTOCOL

    ENGINE     = PyGomo.Engine(enginePath)
    PROTOCOL   = PyGomo.GomocupProtocol()
    CONTROLLER = PyGomo.Controller()

    CONTROLLER.setProtocol(PROTOCOL)
    CONTROLLER.setEngine(ENGINE)


def initEngine(time):
    global CONTROLLER
    config = {
            'timeout_match': -1,
            'timeout_turn' : time,
            'game_type'    : 1,
            'rule'         : 1,
            'thread_num'   : 4
            }
    CONTROLLER.setConfigures(config)
    CONTROLLER.setTimeMatch(5400000)
    CONTROLLER.setTimeLeft(config['timeout_match'])
    return CONTROLLER.isReady()


def deriveSimpleEngine(board, size):
    global CONTROLLER, ENGINE, PROTOCOL
    CONTROLLER.quit()
    del CONTROLLER
    del ENGINE
    del PROTOCOL
    loadEngine('pbrain_minimax.exe')
    CONTROLLER.setTimeMatch(10000)
    CONTROLLER.setTimeLeft(10000)

    move = getMoveFromBoard(board)
    if move is None:
        CONTROLLER.send('begin')
    else:
        CONTROLLER.playMove(move)
    engineMove = CONTROLLER.get('move')
    engineMove = (engineMove.split(',')[0], engineMove.split(',')[1])
    return engineMove
    

def get_move(board, size, time):
    global CONTROLLER
    timeStart = clock()
    # Derive Engine
    if size <= 10:
        return deriveSimpleEngine(board, size)


    if TIME is Ellipsis:
        TIME = int(time * 1000)
        if not initEngine(time):
            # Can't load engine [Error]
            exit()

    move = getMoveFromBoard(board)
    if move is None:
        CONTROLLER.send('begin')
    else:
        CONTROLLER.playMove(move)
    engineMove = CONTROLLER.get('move')
    engineMove = (engineMove.split(',')[0], engineMove.split(',')[1])
    
    timeStop = clock()
    CONTROLLER.calcTimeLeft(int(round(timeStop - timeStart, 3)) * 1000)
    return engineMove
