import socket
from threading import Thread

HOST = ""
PORT = 5000
HEADER_SIZE = 1024

HTTP_RESPONSE = b"""HTTP/1.1 200 OK

<html>
  <p>this thing <em>works</em>!</p>
</html>
"""

class Request:
    def __init__(self, request):
        request = request.decode("utf-8")

        header, body = request.split("\r\n\r\n", 1)
        request_line, *header_list = header.split("\r\n")

        self.request_line = request_line        
        self.headers = Request.parse_headers(header_list)
        self.body = body

    @staticmethod
    def parse_headers(header_list):
        headers = {}
        for header in header_list:
            key, value = header.split(":", 1)
            headers[key.lower()] = value.lstrip()
        return headers

def handle_request(conn, addr):
    request = Request(conn.recv(HEADER_SIZE))
    with conn:
        conn.sendall(HTTP_RESPONSE)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        Thread(target=handle_request, args=(conn, addr)).start()
