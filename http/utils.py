"""In this module are defined several utility classes.

The classes and methods defined have the purpose of giving the library user the
ability of defining the server configuration.
"""


class HttpStatusCode:
    """Class to define the return status codes for the server responses."""

    OK = {
        'code': 200,
        'description': "Status OK."
        }
    CREATED = {
        'code': 201,
        'description': "Resoruce created."
        }
    ACCEPTED = {
        'code': 202,
        'description': "Request accepted."
        }
    NO_CONTENT = {
        'code': 204,
        'description': "Ths resource has no content."
        }
    BAD_REQUEST = {
        'code': 400,
        'description': "Bad request."
        }
    UNAUTHORIZED = {
        'code': 401,
        'description': "Unauthorized access to the requested resource."
        }
    FORBIDDEN = {
        'code': 403,
        'description': "Forbidden access to this resource."
        }

    NOT_FOUND = {
        'code': 404,
        'description': "Resource not found in this server."
        }

    INTERNAL_ERROR = {
        'code': 500,
        'description': "Internal server error."
    }

    NOT_IMPLEMENTED = {
        'code': 501,
        'description': "This service is not implemented in this server."
    }
