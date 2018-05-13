class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, methods):
        def register_route(handler):
            if path in self.routes:
                raise Exception(f"Route '{path}' already registered!")
            self.routes[path] = {}
            for method in methods:
                self.routes[path][method] = handler

            return handler
        return register_route

    def handle_route(self, request, response):
        route = self.routes.get(request.path)
        if route is None:
            response.status_code = 404
            return
        handler = route.get(request.method)
        if handler is None:
            response.status_code = 405
            return
        try:
            handler(request, response)
        except Exception:
            response.status_code = 500
