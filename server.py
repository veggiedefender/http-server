import socket
from threading import Thread
from plumbing import Request


class Server:
    def __init__(self, port=5000, host="", header_size=1024):
        self.port = port
        self.host = host
        self.header_size = header_size

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(1)
            print(f"Listening on http://{socket.getfqdn()}:{self.port}/")
            while True:
                conn, addr = sock.accept()
                Thread(target=self.handle_request, args=(conn, addr)).start()

    def handle_request(self, conn, addr):
        request = Request(conn.recv(self.header_size))
        with conn:
            response = f"""HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
  <h1>Your request:</h1>
  <ul>
    <li>method: {request.method}</li>
    <li>uri: {request.uri}</li>
    <li>http_version: {request.http_version}</li>
    <li>headers: {request.headers}</li>
    <li>body: {request.body}</li>
  </ul>
</html>
"""
            conn.sendall(response.encode("utf-8"))
