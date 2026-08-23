INSERT INTO positions (
    game_id,
    ply,
    fen_before,
    move_uci,
    fen_after,
    turn,
    created_at
) VALUES (
    :game_id,
    :ply,
    :fen_before,
    :move_uci,
    :fen_after,
    :turn,
    :created_at
);
