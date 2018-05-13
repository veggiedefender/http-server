# http-server

A minimal, probably-definitely-not-RFC-compliant HTTP server with an almost
flask-ish API implemented from scratch using Python sockets and threads

Don't use this for anything serious.

## Dependencies
Zero outside of the standard library, of which this project only uses `socket` and `threading`.

This means you can clone and run this right away!

**Note:** Use python 3.6 or higher, because this uses [f-strings](https://www.python.org/dev/peps/pep-0498/).

## Running
```
$ python app.py
```

## What do you mean "flask-ish?"
It looks kind of like Flask on the surface (mainly the decorator based routing)

#### Flask:
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

#### This thing:
```python
from server import Server
app = Server()

@app.route("/")
def hello(request, response):
    response.body = "Hello World!"
```

## Limitations
* Does not implement all or most of HTTP
* Pretty bad at the parts of HTTP it does implement
* Super brittle, probably
* See [issues](https://github.com/veggiedefender/http-server/issues)
