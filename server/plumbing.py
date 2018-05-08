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
