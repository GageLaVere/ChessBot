import torch


class Encoder():

    def __init__(self):

        self.exists = True

        self.P = 0
        self.N = 1
        self.B = 2
        self.R = 3
        self.Q = 4
        self.K = 5
        self.p = 6
        self.n = 7
        self.b = 8
        self.r = 9
        self.q = 10
        self.k = 11

        self.piece_to_plane = {
            "P": self.P,
            "N": self.N,
            "B": self.B,
            "R": self.R,
            "Q": self.Q,
            "K": self.K,
            "p": self.p,
            "n": self.n,
            "b": self.b,
            "r": self.r,
            "q": self.q,
            "k": self.k,
        }


    def encode_fen(self, FEN):
        """Takes a board in FEN Format and encodes to a python list,
            formatted like a tensor. """

        #only take piece portion of FEN
        board_part = FEN.split()[0]

        #create empty planes to encode with 1's
        planes = self.empty_planes()

        #setup the loop
        row = 0
        col = 0

        #example FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        #/ means move to next row
        #a digit means skip that many squares (fill with 0's)
        #letter means to place a 1 on the matching piece plane

        for char in board_part:

            if char == "/":
                row += 1
                col = 0
                continue

            if char.isdigit():
                col += int(char)
                continue

            plane = self.piece_to_plane[char]
            planes[plane][row][col] = 1
            col += 1

        return planes

    def encode_fen_tensor(self, FEN):
        "Takes a board in FEN Format and encodes to a PyTorch tensor."

        planes = self.encode_fen(FEN)

        return torch.tensor(planes, dtype=torch.float32)

    def sum_all(self, FEN):

        planes = self.encode_fen(FEN)

        return sum(
            square
            for plane in planes
            for row in plane
            for square in row
        )


    def sum_p(self, FEN):

        planes = self.encode_fen(FEN)

        return sum(
            square
            for row in planes[self.P]
            for square in row
        )

    def sum_k(self, FEN):

        planes = self.encode_fen(FEN)

        return sum(
            square
            for row in planes[self.k]
            for square in row
        )

    def empty_planes(self):

        return [
            [
                [0 for _ in range(8)]
                for _ in range(8)
            ]
            for _ in range(12)
        ]
