"""Defines server helper methods."""
from http.server import HTTPServer, BaseHTTPRequestHandler
from .http.utils import HttpStatusCode
from .endpoints.endpoint import RestEndpoint
import re


class URLPathResolver(object):
    """This class is a helper to resolve handlers for URL Paths."""

    def __init__(self, urlpatterns):
        """Initialize the urlpatterns of the resolver."""
        self.urlpatterns = urlpatterns

    def resolve(self, url):
        """Resolve the URL and returns Handler.

        If no handler is defined for the url then this method raise an
        URLNotServedException
        """
        for k in self.urlpatterns:
            print('Testing ', url, ' against pattern: ', k)
            if re.search(k, url, re.IGNORECASE):
                return self.urlpatterns[k]
        raise Exception()


class GenericRequestHandler(BaseHTTPRequestHandler):
    """Test HTTP Server."""

    urlpatterns = None

    def delegate(self, method_name):
        """Delegate to the correct handler method."""
        # try:
        resolver = URLPathResolver(GenericRequestHandler.urlpatterns)
        handler = resolver.resolve(self.path.__str__())()
        handler.httpHandler = self
        method = getattr(handler, method_name)
        print('Method: ', method.__name__)
        method()
        print('After Method: ', method.__name__)
        # except:
        # self.send_response(
        #     HttpStatusCode.NOT_IMPLEMENTED['code']
        #     )
        # self.end_headers()
        # self.wfile.write(
        #         bytes(
        #                 HttpStatusCode.NOT_IMPLEMENTED['description'],
        #                 "utf8"
        #             )
        #     )

    def do_GET(self):
        """Server GET Method in a generic way."""
        self.delegate('do_GET')
        return

    def do_POST(self):
        """Server POST Method in a generic way."""
        self.delegate('do_POST')
        return

    def do_PUT(self):
        """Server PUT Method in a generic way."""
        self.delegate('do_PUT')
        return

    def do_OPTIONS(self):
        """Server OPTIONS Method in a generic way."""
        self.delegate('do_OPTIONS')
        return

    def do_DELETE(self):
        """Server DELETE Method in a generic way."""
        self.delegate('do_DELETE')
        return


endpoints = {}


def run(server_ip, server_port):
    """Run the server.

    Runs the server using the configuration passed by parameters. It uses a
    generic implementation of handler used to handle all requests.
    """
    global endpoints
    print('starting server at ', server_ip, ':', server_port, ' ...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server,
    # you need root access
    server_address = (server_ip, server_port)
    GenericRequestHandler.urlpatterns = endpoints
    httpd = HTTPServer(server_address, GenericRequestHandler)
    print('running server...')
    print('serving: ')
    for k in endpoints:
        print(k)
    httpd.serve_forever()


def register_endpoint(url, endpoint):
    """Register an endpoint to server."""
    global endpoints
    qPat = r"\??([a-zA-Z1-9]*=[a-zA-Z1-9]*){0,1}(&[a-zA-Z1-9]*=[a-zA-Z1-9]*)?$"
    endpoints[url+qPat] = endpoint


def route(path, methods=['get']):
    def do(fn):
        """Decorator for registering an endpoint"""
        class Any(RestEndpoint):
            pass

        def wrapper(*args, **kwargs):
            print('Doing wrapping for path', path, 'on function', fn.__name__)
            return fn(*args, **kwargs)

        for method in methods:
            print('registering ', 'do_' + method, 'on path', path)
            setattr(Any, 'do_' + method, wrapper)

        register_endpoint(path, Any)
        return fn
    return do
