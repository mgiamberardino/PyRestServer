"""This module defines the needed classes and methods for endpoint definition.

Here are defined the base classes for the Endpoints definition.
"""
from ..http.utils import HttpStatusCode


class RestEndpoint(object):
    """This class is the base class for endpoint definiton.

    Base class for URL handlers.

    This class define the methods for handle each HTTP method raising an
    MethodNotHandledException in each one of them.
    """

    def __init__(self):
        """Initialize the base URL Handler."""
        self.response = HttpStatusCode.NOT_FOUND
        self.message = None
        self.headers = None

    def add_header(self, key, value):
        """Append a header to the list."""
        if (self.headers is None):
            self.headers = dict({key: value})
        else:
            self.headers[key] = value

    def prepare_response(self):
        """Prepare the response."""
        self.httpHandler.send_response(self.response['code'])
        if self.headers is not None:
            for h in self.headers:
                print(h, '--> ', self.headers[h])
                self.httpHandler.send_header(h, self.headers[h])
            self.httpHandler.end_headers()
        if (self.message is not None):
            self.httpHandler.wfile.write(bytes(self.message, "utf8"))
        else:
            self.httpHandler.wfile.write(bytes(self.httpHandler.rfile, "utf8"))

    def fill_not_implemented_response(self):
        """Prepare response for not implemented methods."""
        self.response = HttpStatusCode.NOT_IMPLEMENTED['code']
        self.message = HttpStatusCode.NOT_IMPLEMENTED['description']

    def get_path(self):
        """Return the path of the request."""
        return self.httpHandler.path.__str__()

    def do_GET(self):
        """Method to handle GET HTTP method that raise an exception."""
        try:
            self.do_get()
        except NameError:
            self.fill_not_implemented_response()
        self.prepare_response()

    def do_POST(self):
        """Method to handle POST HTTP method that raise an exception."""
        try:
            self.do_post()
        except NameError:
            self.fill_not_implemented_response()
        self.prepare_response()

    def do_DELETE(self):
        """Method to handle DELETE HTTP method that raise an exception."""
        try:
            self.do_delete()
        except NameError:
            self.fill_not_implemented_response()
        self.prepare_response()

    def do_PUT(self):
        """Method to handle PUT HTTP method that raise an exception."""
        try:
            self.do_put()
        except NameError:
            self.fill_not_implemented_response()
        self.prepare_response()

    def do_OPTIONS(self):
        """Method to handle OPTIONS HTTP method that raise an exception."""
        try:
            self.do_options()
        except NameError:
            self.fill_not_implemented_response()
        self.prepare_response()

    def message(self, message):
        """Define the message for the response."""
        self.message = message

    def json(self, data):
        """Respond with a json. This method already adds the header."""
        self.add_header('Content-Type', 'application/json')
        self.message = data

    def status(self, httpStatus):
        """Set the status code object for the response."""
        self.response = httpStatus
