import requests
import sys
import hashlib

for file in sys.argv[1:-1]:
    md5 = hashlib.md5(file).hexdigest()
    headers = {'md5:': md5}
    print headers
    r = requests.post(sys.argv[-1], files={file: open(file, 'rb')})
    print file
print "done"