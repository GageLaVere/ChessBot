import torch
from torch.utils.data import Dataset

from learning.board_encoder import Encoder


class ValueDataset(Dataset):

    def __init__(self, storage, encoder=None):

        self.storage = storage
        self.encoder = encoder or Encoder()
        self.rows = self.storage.training_positions()

    def __len__(self):

        return len(self.rows)

    def __getitem__(self, index):

        fen, value_target = self.rows[index]

        board_tensor = self.encoder.encode_fen_tensor(fen)
        target_tensor = torch.tensor([value_target], dtype=torch.float32)

        return board_tensor, target_tensor
