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

        for item in form.list:
            connection = pymongo.Connection(config.db_host, config.db_port)
            db = connection.blah
            collection = db.files
            name = item.name
            md5 = self.headers.get("md5")
            a = collection.find_one({"name": name})
            if a:  #if file exists in mongodb
                if a["md5"] == md5:  #if md5 in mongodb equals md5 of a file

                    self.send_response(200)
                else:
                    os.remove(name)
                    f = open(name, "w")
                    f.write(item.value)
                    f.close()
                    md5local = hashlib.md5(open(name).read()).hexdigest()
                    if md5 == md5local:
                        files = {"name": name, "md5": md5}
                        collection.insert(files)
                        for host in config.hosts:
                            headers = {'md5': md5}
                            r = requests.post(host + ":" + str(config.port), files={file: open(name, 'rb')},
                                              headers=headers)
                        self.send_response(200)
                    else:
                        os.remove(item.name)
                        self.send_response(500)
            else:  #if file does not exists
                f = open(item.name, "w")
                f.write(item.value)
                f.close()
                md5local = hashlib.md5(open(item.name).read()).hexdigest()
                if md5 == md5local:
                    files = {"name": name, "md5": md5}
                    collection.insert(files)
                    for host in config.hosts:
                        headers = {'md5': md5}
                        r = requests.post(host + ":" + str(config.port), files={file: open(name, 'rb')},
                                          headers=headers)
                    self.send_response(200)
                else:
                    os.remove(item.name)
                    self.send_response(500)


def serve():
    os.chdir(config.directory)
    Handler = ServerHandler
    httpd = MyTCPServer((config.ip, config.port), Handler)
    print "serving at port", config.port
    httpd.serve_forever()


if __name__ == '__main__':
    serve()