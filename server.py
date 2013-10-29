import SimpleHTTPServer
import SocketServer
import cgi
import config
import os
import hashlib
import pymongo
import requests


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

        #md5 = self.headers.get("md5")
        #a = collection.find_one({"md5": md5})
        #if a:
        #    print a
        #else:
        #    print "not a!"
        for item in form.list:
            connection = pymongo.Connection(config.db_host, config.db_port)
            db = connection.blah
            collection = db.files
            name = item.name
            md5 = self.headers.get("md5")
            a = collection.find_one({"name": name})
            if a:
                if a["md5"] == md5:
                    print "exists!"
                else:
                    f = open(item.name, "w")
                    f.write(item.value)
                    f.close()
                    md5Local = hashlib.md5(open(item.name).read()).hexdigest()

                if md5 == md5Local:
                    files = {"name": name, "md5": md5}
                    collection.insert(files)
                    self.send_response(200)
                else:
                    self.send_response(500)


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
        md5Local = hashlib.md5(open(filename).read()).hexdigest()
        md5 = self.headers.get("md5")
        if md5 == md5Local:
            files = {"name": filename, "md5": md5}
            connection = pymongo.Connection(config.db_host, config.db_port)
            db = connection.blah
            collection = db.files
            collection.insert(files)
            self.send_response(200)
        else:
            self.send_response(500)


def serve():
    os.chdir(config.directory)
    Handler = ServerHandler
    httpd = MyTCPServer((config.ip, config.port), Handler)
    print "serving at port", config.port
    httpd.serve_forever()

    if __name__ == '__main__':
        serve()