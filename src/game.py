import chess
import time

from player import ChessPlayer

import random

class LiChessGame():

    def __init__(self):

        self.exists = True

class LocalGame():

    def __init__(self, gui_telemetry):

        self.player = None

        self.board = chess.Board()

        self.move_count = 0

        self.gui_telemetry = gui_telemetry


    def create_local_game(self):

        self.board = chess.Board()

        print(self.board)

        self.game_active = True

    def play_local(self):

        self.create_local_game()

        while self.game_active:

            self.play_round()

            if self.board.is_game_over():
                print(self.board.result())
                self.game_active = False

            #150 moves each
            if self.move_count > 300:
                self.game_active = False

        self.reset()

    def reset(self):

        self.player = None

        self.board = chess.Board()

        self.move_count = 0

    def play_round(self):

        #langgraph thought process here

        self.make_move()

        #save here
        
        self.move_count += 1

    def decide_move(self):

        legal_moves = list(self.board.legal_moves)

        if legal_moves:
            return random.choice(legal_moves)

    def make_move(self):

        move = self.decide_move()

        if move is None:
            self.game_active = False
            return

        self.board.push(move)

        #print("\n", self.board.fen(), "\n")

        self.gui_telemetry.send_fen(self.board.fen())

        #print("\n", self.board, "\n")

        time.sleep(.5)
