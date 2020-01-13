import socket
import time

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False


starttime=time.time()

while True:
    print("Testing")
    if isOpen('207.216.103.218', 30266):
    # if isOpen('localhost', 30266):
        print('Success')
    else:
        print('Fail')
    time.sleep(3.0 - (time.time() % 3.0))
