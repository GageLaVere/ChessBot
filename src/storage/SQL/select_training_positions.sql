SELECT
    fen_before,
    value_target
FROM positions
WHERE value_target IS NOT NULL
ORDER BY game_id, ply;
