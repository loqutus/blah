import SocketServer

import requests

import config


#without this, server not restarting
class MyTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True

#check, if file exists and it's md5 is correct
def check_if_file_exists:


#upload file to other servers


    def upload_file(self, filename):
        for host in config.hosts:
            head = {'md5': md5}
            print "Uploading " + filename + "to " + host + ":" + str(config.port) + ", " + head
            fil = open(config.directory + "/" + name, 'rb')
            r = requests.post("http://" + host + ":" + str(config.port), files={file: fil},
                              headers=head)
            file.close()