import requests
import sys

for file in sys.argv[1:-1]:
    r = requests.post(sys.argv[-1], files={file: open(file, 'rb')})
    print file
print "done"