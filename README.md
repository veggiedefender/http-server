# http-server

A minimal, probably-definitely-not-RFC-compliant HTTP server with an almost
flask-ish API implemented from scratch using Python sockets and threads

## Dependencies
Zero outside of the standard library, of which this project only uses `socket` and `threading`.

This means you can clone and run this right away!

**Note:** Use python 3.6 or higher, because this uses [f-strings](https://www.python.org/dev/peps/pep-0498/).

## Running
```
$ python app.py
```

## What do you mean "flask-ish?"
I tried to implement the more surface-level Flask API features:

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
def hello():
    return "Hello World!"
```

## Limitations
* Does not implement all or most of HTTP
* Pretty bad at the parts of HTTP it does implement
* Super brittle, probably
* Literally the only error handling comes from request threads not killing the main thread
* See [issues](https://github.com/veggiedefender/http-server/issues)
