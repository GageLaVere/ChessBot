import socket

class Telemetry():

    def __init__(self):

            
        self.HOST = '127.0.0.1'
        self.PORT = 8001

        self.server = None
        self.conn = None

        try: 
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.HOST, self.PORT))
            self.server.listen(1)
            self.server.setblocking(False)

            print(f"\nStarted server on {self.HOST}:{self.PORT}\n")

        except Exception as e:
            print("Error opening Telemetry server! With Error: \n", e)
            if self.server is not None:
                self.server.close()
            self.server = None
            



        self.running = True
        self.last_fen = b""


    def send_fen(self, fen):

        self.last_fen = f"{fen}\n".encode("utf-8")

        if self.server is None:
            return

        if self.conn is None:
            try:
                self.conn, addr = self.server.accept()
                print(f"\nConnected with: {addr}\n")
            except BlockingIOError:
                return
            except OSError:
                return

        try:
            self.conn.sendall(self.last_fen)
        except OSError:
            self.conn.close()
            self.conn = None
