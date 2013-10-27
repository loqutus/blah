import SimpleHTTPServer
import SocketServer
import cgi
import config
import os


class MyTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
            })
        for item in form.list:
            f = open(item.name, "w")
            print item.name
            f.write(item.value)
            f.close()
        self.send_response(200)

    def do_PUT(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'PUT',
            })
        filename = self.headers.get("File")
        tmp = form.file
        result = tmp.read()
        fl = open(filename, "wb")
        fl.write(result)
        fl.close()
        self.send_response(200)


def serve():
    os.chdir(config.directory)
    Handler = ServerHandler
    httpd = MyTCPServer((config.ip, config.port), Handler)
    print "serving at port", config.port
    httpd.serve_forever()


if __name__ == '__main__':
    serve()