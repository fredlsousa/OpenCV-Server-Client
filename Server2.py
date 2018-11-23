import socket
import cv2
import numpy
import thread


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def newClient(clientsocket, addr):
    while True:
        length = recvall(clientsocket, 16)
        stringData = recvall(clientsocket, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg = cv2.imdecode(data, 1)
        cv2.imwrite('rec%s.jpg', decimg)
    clientsocket.close()

TCP_IP = '192.168.100.109'
TCP_PORT = 4040

print 'Launching Server...'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)

print 'Server Launched!'
print 'Waiting for clients...'

while True:
    conn, addr = s.accept()
    print 'Connection started, from: ', addr
    thread.start_new_thread(newClient, (conn, addr))

s.close()