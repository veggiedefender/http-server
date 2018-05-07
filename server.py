import socket

HOST = ""
PORT = 5000
HEADER_SIZE = 1024

HTTP_RESPONSE = b"""HTTP/1.1 200 OK

<html>
  <p>this thing <em>works</em>!</p>
</html>
"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        request = conn.recv(HEADER_SIZE)
        with conn:
            conn.sendall(HTTP_RESPONSE)
