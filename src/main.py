import subprocess
import sys
from pathlib import Path

from game import LocalGame
from gui_telemetry import Telemetry


class System():

    def __init__(self):
        self.running = True

        self.any_game_active = False
        self.viewer_process = None
        self.gui_telemetry = Telemetry()

        self.run()

    def run(self):
        try:
            while self.running == True:
                self.play_local_game()
        finally:
            self.stop_viewer()

    def play_local_game(self):

        self.game = LocalGame(self.gui_telemetry)
        self.start_viewer()

        self.any_game_active = True
        self.game.play_local()
        self.any_game_active = False

    def start_viewer(self):

        if self.viewer_process is not None:
            return

        project_root = Path(__file__).resolve().parents[1]
        viewer_path = project_root / "chess_gui" / "main.py"

        self.viewer_process = subprocess.Popen(
            [sys.executable, str(viewer_path)],
            cwd=project_root)

    def stop_viewer(self):

        if self.viewer_process is None:
            return

        self.viewer_process.terminate()
        try:
            self.viewer_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.viewer_process.kill()
            self.viewer_process.wait()
        self.viewer_process = None


if __name__ == "__main__":
    system = System()
