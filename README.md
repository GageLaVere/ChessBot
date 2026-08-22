# Chess Bot

## Current Behavior

- Starts a local chess game.
- Chooses random legal moves.
- Prints the board/FEN in the terminal.
- Sends FEN updates over TCP on `127.0.0.1:8001`.
- Launches a PySide6 viewer that renders the live board.

## Direction

The next project milestones are:

```text
game logging
board encoding
PyTorch value model
training/evaluation loop
Lichess bot integration
daily model promotion
```

The goal is to build an optimal ML loop that records data, trains models, evaluates candidates, and improves over time, not neccessarily immediate play strength


## Current Architecture

```text
src/
  main.py            bot process entry point
  game.py            local game loop and random legal move selection
  gui_telemetry.py   TCP server that publishes board FEN updates
  graph.py           early LangGraph move workflow scaffold
  cli.py             older terminal play-against-bot entry point
  player.py          placeholder player abstraction

chess_gui/
  main.py            PySide6 desktop viewer process
```

The bot process is the TCP server. The viewer process is the TCP client.

```text
bot process
  owns chess board state
  makes moves
  sends latest FEN over localhost TCP

viewer process
  connects to the bot
  receives FEN strings
  renders a small always-on-top chess board
```

## Dependencies

Core dependencies are declared in `pyproject.toml`:

```text
python-chess
langgraph
PySide6
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

From the project root:

```bash
python -m src.main
```

or:

```bash
python src/main.py
```

The bot will start a local game and launch the viewer process automatically.