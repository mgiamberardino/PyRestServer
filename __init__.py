"""Helper to define REST APIs.

You can use this module to define and run a REST API server.
You can run a server from a simple line:
    from rest import server
    server.run ('server_ip',server_port)
This server does not serve any endpoint so is pointless. You can use some of
the utilities methods to add endpoints to the server.

To register an endpoint first you have to create one. To create a new endpoint
you have to extend the RestEndpoint class from the rest.endpoint module and
implement the correct methods to serve.
If you want to define an endpoint serving GET and POST methods you have to
define the methods 'do_get(self)' and 'do_post(self)' on your endpoin class.

You can also implement other methods:

    PUT: do_put(self)
    OPTIONS: do_options(self)
    DELETE: do_delete(self)

Once you have the class defined you have to register it using the
server.register_endpoint('path', endpoint_class).

After defining all your endpoints you can run the server a try it.
"""
