UPDATE positions
SET
    result = :result,
    value_target = CASE
        WHEN :result = '1/2-1/2' THEN 0.0
        WHEN :result = '1-0' AND turn = 'white' THEN 1.0
        WHEN :result = '1-0' AND turn = 'black' THEN -1.0
        WHEN :result = '0-1' AND turn = 'white' THEN -1.0
        WHEN :result = '0-1' AND turn = 'black' THEN 1.0
        ELSE NULL
    END
WHERE game_id = :game_id;
