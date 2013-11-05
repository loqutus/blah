import SimpleHTTPServer
import SocketServer
import cgi
import config
import os
import hashlib
import pymongo
import requests
#import pdb


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
            print a
            if a:  #if file exists in mongodb
                if a["md5"] == md5:  #if md5 in mongodb equals md5 of a file
                    print "1"
                    if os.path.exists(name):
                        print "2"
                        md5local = hashlib.md5(open(name).read()).hexdigest()
                        if md5local == md5:
                            print "3"
                            pass
                        else:
                            print "4"
                            os.remove(name)
                            f = open(name, "w")
                            f.write(item.value)
                            f.close()
                    else:
                        print "5"
                        f = open(name, "w")
                        f.write(item.value)
                        f.close()
                    self.send_response(200)
                else:
                    print "6"
                    os.remove(name)
                    f = open(name, "w")
                    f.write(item.value)
                    f.close()
                    md5local = hashlib.md5(open(name).read()).hexdigest()
                    if md5 == md5local:
                        print "7"
                        files = {"name": name, "md5": md5}
                        collection.insert(files)
                        #pdb.set_trace()
                        for host in config.hosts:
                            print host
                            print "http://" + host + ":" + str(config.port)
                            print config.directory + "/" + name
                            head = {'md5': md5}
                            print head
                            fil = open(config.directory + "/" + name, 'rb')
                            r = requests.post("http://" + host + ":" + str(config.port),
                                              files=fil, headers=head)
                            fil.close()
                        self.send_response(200)
                    else:
                        print 8
                        os.remove(name)
                        self.send_response(500)
            else:  #if file does not exist
                print 9
                f = open(name, "w")
                f.write(item.value)
                f.close()
                md5local = hashlib.md5(open(name).read()).hexdigest()
                if md5 == md5local:
                    print 10
                    files = {"name": name, "md5": md5}
                    collection.insert(files)
                    for host in config.hosts:
                        print host
                        print "http://" + host + ":" + str(config.port)
                        #pdb.set_trace()
                        head = {'md5': md5}
                        fil = open(config.directory + "/" + name, 'rb')
                        r = requests.post("http://" + host + ":" + str(config.port), files=fil,
                                          headers=head)
                        file.close()
                    self.send_response(200)
                else:
                    print "11"
                    os.remove(name)
                    self.send_response(500)


def serve():
    os.chdir(config.directory)
    Handler = ServerHandler
    httpd = MyTCPServer((config.ip, config.port), Handler)
    print "serving at port", config.port
    httpd.serve_forever()


if __name__ == '__main__':
    serve()
