import requests
import sys
import hashlib

for file in sys.argv[1:-1]:
    md5 = hashlib.md5(file)
    headers = {'md5': md5}
    r = requests.post(sys.argv[-1], files={file: open(file, 'rb')}, headers=headers)
    print file
print "done"