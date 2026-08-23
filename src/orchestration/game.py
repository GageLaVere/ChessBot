import chess
import time

from orchestration.player import ChessPlayer
import random

class LiChessGame():

    def __init__(self):

        self.SOURCE = "local_self_play"

        self.exists = True

class LocalGame():


    def __init__(self, gui_telemetry, storage, 
                 WHITE_PLAYER, BLACK_PLAYER, SOURCE):

        self.SOURCE = SOURCE
        self.WHITE_PLAYER = WHITE_PLAYER
        self.BLACK_PLAYER =  BLACK_PLAYER

        self.board = chess.Board()

        self.move_count = 0
        self.game_id = None

        self.storage = storage
        self.gui_telemetry = gui_telemetry


    def create_local_game(self):

        self.board = chess.Board()

        #print(self.board)

        self.game_active = True

        self.game_id = self.storage.start_game(
            self.SOURCE,
            self.WHITE_PLAYER,
            self.BLACK_PLAYER,
        )

    def play_local(self):

        self.create_local_game()

        while self.game_active:

            self.play_round()

            if self.board.is_game_over():
                print(self.board.result())
                self.finish_game("game_over")
                self.game_active = False

            if self.move_count > 300:
                self.finish_game("move_cap")
                self.game_active = False

        self.reset()

    def finish_game(self, termination):

        if self.game_id is None:
            return

        self.storage.finish_game(
            self.game_id,
            self.board.result(claim_draw=True),
            termination,
            self.move_count,
        )
        self.game_id = None

    def reset(self):

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

        fen_before = self.board.fen()
        turn = "white" if self.board.turn == chess.WHITE else "black"

        self.board.push(move)
        fen_after = self.board.fen()

        if self.game_id is not None:
            self.storage.log_position(
                self.game_id,
                self.move_count,
                fen_before,
                move.uci(),
                fen_after,
                turn,
            )

        #print("\n", self.board.fen(), "\n")

        self.gui_telemetry.send_fen(self.board.fen())

        #print("\n", self.board, "\n")

        time.sleep(.5)
