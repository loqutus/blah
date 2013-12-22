import SimpleHTTPServer
import SocketServer
import cgi
import os
import hashlib

import config
import pymongo
import requests

#without this, server not restarting
class MyTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True

#check, if file exists and it's md5 is correct
def check_if_file_exists():

#connect to mongo db
def mongo_connect():
    connection = pymongo.Connection(config.db_host, config.db_port)
    db = connection.blah
    global collection = db.files

#get data from post request
def get_request():
    form = cgi.FieldStorage(
        fp=self.rfile,
        global headers=headers,
                   environ = {'REQUEST_METHOD': 'POST',
                              'CONTENT_TYPE': headers['Content-Type'],})

#upload file to other servers
def upload_file(self, filename):
    for host in config.hosts:
        head = {'md5': md5}
        print "Uploading " + filename + "to " + host + ":" + str(config.port) + ", " + head
        fil = open(config.directory + "/" + name, 'rb')
        r = requests.post("http://" + host + ":" + str(config.port), files={file: fil},
                          headers=head)
        file.close()


if __name__ == "__main__":
    os.chdir(config.directory)
    Handler = ServerHandler
    httpd = MyTCPServer((config.ip, config.port), Handler)
    print "serving at port", config.port
    httpd.serve_forever()