import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from storage.sql_queries import (
    CREATE_TABLES_SQL,
    INSERT_GAME_SQL,
    INSERT_POSITION_SQL,
    UPDATE_GAME_RESULT_SQL,
    UPDATE_POSITION_TARGETS_SQL,
    SELECT_TRAINING_POSITIONS_SQL,
    COUNT_GAMES_SQL,
    COUNT_POSITIONS_SQL,
    COUNT_TRAINING_POSITIONS_SQL,
    SELECT_LATEST_GAME_SQL,
)

class GameStorage():

    def __init__(self, db_path=None):

        if db_path is None:
            db_path = Path(__file__).resolve().parents[2] / "data" / "chess_bot.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")

        self.initialize_schema()

    def initialize_schema(self):

        self.connection.executescript(CREATE_TABLES_SQL)
        self.connection.commit()

    def start_game(self, source, white_player, black_player):

        game_id = f"{source}_{self._utc_now_compact()}_{uuid4().hex[:8]}"

        self.connection.execute(
            INSERT_GAME_SQL,
            {
                "id": game_id,
                "source": source,
                "started_at": self._utc_now(),
                "white_player": white_player,
                "black_player": black_player,
            },
        )
        self.connection.commit()

        return game_id

    def log_position(self, game_id, ply, fen_before, move_uci, fen_after, turn):

        self.connection.execute(
            INSERT_POSITION_SQL,
            {
                "game_id": game_id,
                "ply": ply,
                "fen_before": fen_before,
                "move_uci": move_uci,
                "fen_after": fen_after,
                "turn": turn,
                "created_at": self._utc_now(),
            },
        )
        self.connection.commit()

    def finish_game(self, game_id, result, termination, plies):

        self.connection.execute(
            UPDATE_GAME_RESULT_SQL,
            {
                "id": game_id,
                "ended_at": self._utc_now(),
                "result": result,
                "termination": termination,
                "plies": plies,
            },
        )
        self.connection.execute(
            UPDATE_POSITION_TARGETS_SQL,
            {
                "game_id": game_id,
                "result": result,
            },
        )
        self.connection.commit()

    def training_positions(self):

        return self.connection.execute(SELECT_TRAINING_POSITIONS_SQL).fetchall()

    def summary(self):

        latest_game = self.connection.execute(SELECT_LATEST_GAME_SQL).fetchone()

        return {
            "games": self.connection.execute(COUNT_GAMES_SQL).fetchone()[0],
            "positions": self.connection.execute(COUNT_POSITIONS_SQL).fetchone()[0],
            "training_positions": self.connection.execute(COUNT_TRAINING_POSITIONS_SQL).fetchone()[0],
            "latest_game": latest_game,
        }

    def close(self):

        self.connection.close()

    def _utc_now(self):

        return datetime.now(timezone.utc).isoformat()

    def _utc_now_compact(self):

        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
