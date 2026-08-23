UPDATE games
SET
    ended_at = :ended_at,
    result = :result,
    termination = :termination,
    plies = :plies
WHERE id = :id;
