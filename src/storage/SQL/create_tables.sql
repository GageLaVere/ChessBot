CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    result TEXT,
    termination TEXT,
    plies INTEGER NOT NULL DEFAULT 0,
    white_player TEXT NOT NULL,
    black_player TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    ply INTEGER NOT NULL,
    fen_before TEXT NOT NULL,
    move_uci TEXT NOT NULL,
    fen_after TEXT NOT NULL,
    turn TEXT NOT NULL,
    result TEXT,
    value_target REAL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE INDEX IF NOT EXISTS idx_positions_game_id ON positions(game_id);
CREATE INDEX IF NOT EXISTS idx_positions_value_target ON positions(value_target);
