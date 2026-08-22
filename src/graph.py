from __future__ import annotations

import random
from typing import TypedDict

import chess
from langgraph.graph import END, START, StateGraph


class GameState(TypedDict):
    fen: str
    human_move: str
    bot_move: str | None
    error: str | None
    game_over: bool
    result: str | None


def validate_human_move(state: GameState) -> dict:
    board = chess.Board(state["fen"])
    raw_move = state["human_move"].strip()

    try:
        move = chess.Move.from_uci(raw_move)
    except ValueError:
        return {"error": f"'{raw_move}' is not UCI format. Try moves like e2e4 or g1f3."}

    if move not in board.legal_moves:
        return {"error": f"'{raw_move}' is not legal in this position."}

    return {"error": None}


def apply_human_move(state: GameState) -> dict:
    board = chess.Board(state["fen"])
    board.push(chess.Move.from_uci(state["human_move"].strip()))
    return _board_update(board)


def choose_bot_move(state: GameState) -> dict:
    board = chess.Board(state["fen"])

    if board.is_game_over():
        return _board_update(board)

    move = random.choice(list(board.legal_moves))
    board.push(move)
    return {"bot_move": move.uci(), **_board_update(board)}


def _board_update(board: chess.Board) -> dict:
    return {
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    }


def route_after_validation(state: GameState):
    if state["error"]:
        return END
    return "apply_human_move"


def route_after_human_move(state: GameState):
    if state["game_over"]:
        return END
    return "choose_bot_move"


def build_graph():
    builder = StateGraph(GameState)
    builder.add_node("validate_human_move", validate_human_move)
    builder.add_node("apply_human_move", apply_human_move)
    builder.add_node("choose_bot_move", choose_bot_move)

    builder.add_edge(START, "validate_human_move")
    builder.add_conditional_edges("validate_human_move", route_after_validation)
    builder.add_conditional_edges("apply_human_move", route_after_human_move)
    builder.add_edge("choose_bot_move", END)

    return builder.compile()
