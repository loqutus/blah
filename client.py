import sys
import hashlib

import requests

print "1"
print sys.argv[0]
print sys.argv[1]
file = sys.argv[1]
print "2"
#todo:use basename instead of just sys.argv[]
md5 = hashlib.md5(open(file).read()).hexdigest()
headers = {'md5': md5}
print md5
print headers
print file
print sys.argv[-1]
r = requests.post(sys.argv[-1], files={file: open(file, 'rb')}, headers=headers)
print file
print "done"
