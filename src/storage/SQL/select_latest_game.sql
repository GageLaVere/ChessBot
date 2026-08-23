SELECT
    id,
    source,
    white_player,
    black_player,
    result,
    termination,
    plies,
    started_at,
    ended_at
FROM games
ORDER BY started_at DESC
LIMIT 1;
