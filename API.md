# API & Design Docs

## Basic Usage

```python
from server import Server
app = Server()

@app.route("/")
def hello(request, response):
    response.body = "Hello World!"

if __name__ == "__main__":
    app.start()
```

Save this in `app.py`.

## Request lifecycle (high level overview)

When a browser sends a request to the server, the following happens:
1. Spawn a new thread to handle the connection
2. Read [`header_size`](#customizing-the-server) bytes from the connection
3. Parse the HTTP request into a [`Request`](#request) object
4. Build a [`Response`](#response) object
4. Match the request to a [handler](#request-handlers) based on the request's
   path, then HTTP method
5. Call the [handler](#request-handlers), passing in the [`Request`](#request)
   and [`Response`](#response) objects built for that request
6. The [handler](#request-handlers) modifies the [`Response`](#response) and
   exits
7. Build a properly formatted HTTP response from the [`Response`](#response)
   object.
8. Send the response to the browser, as `utf-8` encoded bytes.

## API

### Customizing the server

All customizations are passed as keyword arguments to `app.start()`.

Argument | Description | Default
--- | --- | ---
`port` | The TCP port the server will listen on | `5000`
`host` | Address the server will listen from. Use `0.0.0.0` to listen on all assigned addresses | `""` (localhost)
`header_size` | Max size of a request, in bytes, that the server will accept | `1024`

You may monkey-patch or override class methods, but figuring out how to do that
is up to you.

### Request Handlers

Handlers are where the majority of the code you'll write will end up. They
correspond one to many with routes, meaning one handler may map to any number of
paths or methods, but any one path + method combination will map unambiguously
to one handler.

Handlers take exactly **two** arguments: the `request` and `response`, which are
[Request](#request) and [Response](#response) objects, respectively.

Handlers typically output by modifying the `response`.

Use them like this:

```python
@app.route("/path/to/resource")
def descriptive_name(request, response):
    response.body = "Hello World!"
```

Specify HTTP methods like this:

```python
@app.route("/path/to/resource", methods=["GET", "POST"])
def descriptive_name(request, response):
    if request.method == "GET":
        response.body = "Sent a GET request!"
    else if request.method == "POST":
        response.body = "Sent a POST request!"
```

Leaving out the `methods` argument is identical to passing in `methods=["GET"]`.

### Request and Response

Requests and Responses are a thin wrapper over their HTTP counterparts.

#### Request

Attribute | Description | Example
--- | --- | ---
`datetime` | `datetime` object the request was parsed at | `'2018-05-18 22:34:53.669021'`
`ip` | IP address of the connection | `192.168.1.11`
`method` | HTTP method of the request (case sensitive) | `GET`, `POST`, etc.
`uri` | Full URI of the request | `/path/to/resource?q=test&t=100`
`path` | Only the path portion of the `uri` | `/path/to/resource`
`queries` | Dict of queries parsed from the `uri` | `{"q": "test", "t": "100"}`
`http_version` | HTTP version included in the request | `HTTP/1.1`
`headers` | Dict of headers sent in the request | `{"user-agent": "cool dude" }`
`body` | `string` containing the body of the request | `"what's up?"`

Requests may be printed or casted to `str` and will follow this template:

```python
"{method} {uri} {http_version} from {ip} at {date}"
```

#### Response

All of the following attributes can be set by [handlers](#request-handlers),
and they are the main way of sending output back to the browser.

Attribute | Description | Example
--- | --- | ---
`headers` | Dict of headers to send in the response | `{"last-modified": "Fri, 18 May 2018 23:20:44 GMT"}`
`body` | String of the body (HTML, files, etc.) to send back | `"<p>hello world</p>`
`status_code` | Status code of the response | `200`, `500`, etc.
`status_message` | Status message to pair with `status_code`. A sane default will be chosen if left unchanged, but you may set a custom message | `"SERVER MACHINE BROKE"`
