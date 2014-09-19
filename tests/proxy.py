# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

from .server import WithAsyncLoop, Destructing, WithClient, TestServer
from .client import TestClient
import aiocoap.proxy

class WithProxyServer(WithAsyncLoop, Destructing):
    def setUp(self):
        super(WithProxyServer, self).setUp()
        pass
        # FIXME: currently, you need to run ./coap-proxy --forward --server-port 56839 externally.

    proxyaddress = 'localhost:56839'

class WithProxyClient(WithClient, WithProxyServer):
    def setUp(self):
        super(WithProxyClient, self).setUp()
        original_client_log = self.client.log
        self.client = aiocoap.proxy.ProxyForwarder(self.proxyaddress, self.client)
        self.client.log = original_client_log

    def tearDown(self):
        self.client = self.client.context

class TestServerWithProxy(WithProxyClient, TestServer):
    def build_request(self):
        # this needs to be run differently because tests/server.py
        # doesn't exactly use the high-level apis. (and that's ok because we need
        # to test the server with simple messages too.)

        request = aiocoap.Message(code=aiocoap.GET)
        request.unresolved_remote = self.proxyaddress
        request.opt.proxy_scheme = 'coap'
        request.opt.uri_host = self.serveraddress
        return request

# leaving that out for a moment because it fails more slowly

#class TestClientWithProxy(WithProxyClient, TestClient):
#    pass

# no need to run them again
del TestClient
del TestServer
