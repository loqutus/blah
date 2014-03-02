import sys
import hashlib
import cgi

import requests
import SocketServer

action = sys.argv[1]
if action == 'upload':
    file = sys.argv[2]
    md5 = hashlib.md5(open(file).read()).hexdigest()
    headers = {'md5': md5, 'action': 'upload'}
    r = requests.post(sys.argv[3], files={file: open(file, 'rb')}, headers=headers)
elif action == 'download':
    file = sys.argv[2]
    headers = {'file': file, 'action': 'download'}
    r = requests.post(sys.argv[3], headers=headers)
    form = cgi.FieldStorage(
        fp=SocketServer.rfile,
        headers=headers,
        environ={'REQUEST_METHOD': 'POST',
                 'CONTENT_TYPE': headers['Content-Type'],
        })
    print "done"
