from server import Server
from urllib.parse import parse_qs

app = Server()

@app.route("/")
def index(request, response):
    response.body = f"""<!DOCTYPE html>
<html>
<head>
  <title>greeter</title>
</head>
<body>
  <form action="/greet" method="POST">
    <label for="name">
      Enter your name:
      <input type="text" name="name">
    </label>
    <input type="submit">
  </form>
</body>
</html>
"""

@app.route("/greet", methods=["POST"])
def greet(request, response):
    name = parse_qs(request.body)["name"][0]
    response.body = f"""<!DOCTYPE html>
<html>
<head>
  <title>hello!</title>
</head>
<body>
  <p>Hello, {name}!</p>
  <a href="/">try again</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.start(host="0.0.0.0", port=3000)
