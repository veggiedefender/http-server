import socket
from threading import Thread
from plumbing import Request

HOST = ""
PORT = 5000
HEADER_SIZE = 1024

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
