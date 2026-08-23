from pathlib import Path


SQL_DIR = Path(__file__).resolve().parent / "SQL"


def _read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


CREATE_TABLES_SQL = _read_sql("create_tables.sql")
INSERT_GAME_SQL = _read_sql("insert_game.sql")
INSERT_POSITION_SQL = _read_sql("insert_position.sql")
UPDATE_GAME_RESULT_SQL = _read_sql("update_game_result.sql")
UPDATE_POSITION_TARGETS_SQL = _read_sql("update_position_targets.sql")
SELECT_TRAINING_POSITIONS_SQL = _read_sql("select_training_positions.sql")
COUNT_GAMES_SQL = _read_sql("count_games.sql")
COUNT_POSITIONS_SQL = _read_sql("count_positions.sql")
COUNT_TRAINING_POSITIONS_SQL = _read_sql("count_training_positions.sql")
SELECT_LATEST_GAME_SQL = _read_sql("select_latest_game.sql")
