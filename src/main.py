import subprocess
import sys
from pathlib import Path

from orchestration.game import LocalGame
from storage.storage import GameStorage
from interfaces.gui_telemetry import Telemetry


SOURCE = "local_self_play"

#should be reconfigured with langchain nightly,
#for self-improvement
WHITE_PLAYER = "random_v0"
BLACK_PLAYER = "random_v0"

class System():

    def __init__(self):
        self.running = True

        self.any_game_active = False
        self.viewer_process = None
        self.gui_telemetry = Telemetry()
        self.storage = GameStorage()
        self.run()

    def run(self):
        try:
            while self.running == True:
                self.play_local_game()
        except KeyboardInterrupt:
            self.running = False
            if self.any_game_active:
                self.game.finish_game("keyboard_interrupt")
        finally:
            self.stop_viewer()
            self.storage.close()

    def play_local_game(self):

        self.game = LocalGame(self.gui_telemetry, self.storage,
                            WHITE_PLAYER, BLACK_PLAYER, SOURCE)
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
