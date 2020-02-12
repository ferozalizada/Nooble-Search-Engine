from http.server import HTTPServer, BaseHTTPRequestHandler
from modules.user_interface.UserInterface import UserInterface
import json


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/modules/user_interface/user_interface.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        # maybe there is a better way to get POST without libraries
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = post_data.decode('utf-8').split("&")

        POST = {}
        for x in params:
            parts = x.split("=")
            key = parts[0]
            value = parts[1]
            POST.update({key: value})

        UI = UserInterface(POST["query"], POST["model"], POST["collection"])
        docs_collection = UI.getDocs()  # get the collection of docs

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        #self.wfile.write(bytes(docs_collection, 'utf-8'))
        self.wfile.write(json.dumps(docs_collection).encode(encoding='utf_8'))


def start_web_server():
    httpd = HTTPServer(('localhost', 8080), Server)
    print("Web server started on port 8080...")
    httpd.serve_forever()
