import socket
from threading import Thread
from .router import Router
from .plumbing import Request, Response


class Server:
    def __init__(self):
        self.router = Router()

    def start(self, port=5000, host="", header_size=1024):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            print(f"Listening on http://{socket.getfqdn()}:{port}/")
            while True:
                conn, addr = sock.accept()
                Thread(target=self.handle_connection, args=(conn, addr, header_size)).start()

    def handle_connection(self, conn, addr, header_size):
        request_bytes = conn.recv(header_size)
        with conn:
            response = Response()
            try:
                request = Request(request_bytes)
                self.router.handle_route(request, response)
            except Exception:
                response.status_code = 400
            conn.sendall(response.serialize())

    def route(self, uri, methods=None):
        if methods is None:
            methods = ["GET"]
        return self.router.add_route(uri, methods)
