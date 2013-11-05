import requests
import sys
import hashlib

for file in sys.argv[1:-1]:
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
