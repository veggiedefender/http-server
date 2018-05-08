from server import Server

app = Server()

@app.route("/")
def index(request):
    return f"""<!DOCTYPE html>
<html>
  <h1>Your request:</h1>
  <ul>
    <li>method: {request.method}</li>
    <li>uri: {request.uri}</li>
    <li>http_version: {request.http_version}</li>
    <li>headers: {request.headers}</li>
    <li>body: {request.body}</li>
  </ul>
</html>
"""

if __name__ == "__main__":
    app.start()
