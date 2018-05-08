import socket
from threading import Thread

HOST = ""
PORT = 5000
HEADER_SIZE = 1024

class Request:
    def __init__(self, request):
        request = request.decode("utf-8")

        header, body = request.split("\r\n\r\n", 1)
        request_line, *header_list = header.split("\r\n")
        method, uri, http_version = Request.parse_request_line(request_line)

        self.method = method
        self.uri = uri
        self.http_version = http_version
        self.headers = Request.parse_headers(header_list)
        self.body = body

    @staticmethod
    def parse_request_line(request_line):
        method, uri, http_version = request_line.split(" ")
        return method, uri, http_version

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
        HTTP_RESPONSE = f"""HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
  <h1>Your request:</h1>
  <ol>
    <li>method: {request.method}</li>
    <li>uri: {request.uri}</li>
    <li>http_version: {request.http_version}</li>
    <li>headers: {request.headers}</li>
    <li>body: {request.body}</li>
  </ol>
</html>
"""
        conn.sendall(HTTP_RESPONSE.encode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        Thread(target=handle_request, args=(conn, addr)).start()
