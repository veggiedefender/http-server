from .status_codes import status_codes

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

RESPONSE_TEMPLATE = "HTTP/1.1 {status_code} {status_message}\r\n{headers}\r\n{body}"
class Response:
    def __init__(self, headers=None, body="", status_code=200):
        if headers is None:
            headers = {}

        self.headers = headers
        self.body = body
        self.status_code = status_code

    def serialize(self):
        header_list = [f"{key.lower()}: {value}" for key, value in self.headers.items()]
        http_response = RESPONSE_TEMPLATE.format(
            status_code=self.status_code,
            status_message=status_codes.get(self.status_code, "???"),
            headers="\r\n".join(header_list) + "\r\n",
            body=self.body
        )
        return http_response.encode("utf-8")
