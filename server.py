import threading
import time
import urllib.parse

from http.server import BaseHTTPRequestHandler, HTTPServer
from bot import Bot

class Server(object):

    def __init__(self):

        self.hostName = ""
        self.hostPort = 8080

        t = threading.Thread(target=self.StartServer)
        t.daemon = True
        t.start()



    def StartServer(self):

        myServer = HTTPServer((self.hostName, self.hostPort), MyServer)
        print(time.asctime(), "Server Starts - %s:%s" % (self.hostName, self.hostPort))

        try:
            myServer.serve_forever()
        except KeyboardInterrupt:
            pass

        myServer.server_close()
        print(time.asctime(), "Server Stops - %s:%s" % (self.hostName, self.hostPort))

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        path = urllib.parse.urlparse(self.path).path.strip("/")

        token = params.get("token")[0] if params.get("token") else None
        message = params.get("m")[0] if params.get("m") else None

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if path == "send" and token and message:
            Bot().SendMessage(token, message)
            self.wfile.write(bytes("Done", "utf-8"))

        else:
            self.wfile.write(bytes("Unknown method", "utf-8"))
