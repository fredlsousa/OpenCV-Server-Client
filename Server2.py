import socket
import cv2
import numpy
import thread

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')     #Database to identify the faces
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')                      #Database to identify the eyes

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def newClient(clientsocket, addr, i):
    while True:
        length = recvall(clientsocket, 16)
        stringData = recvall(clientsocket, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg = cv2.imdecode(data, 1)
        checkFace = faceRecognition(decimg, i)
        if checkFace == 1:
            cv2.imwrite('received ' + str(i) + '.jpg', decimg)
    clientsocket.close()

def TCP_SOCKET(TCP_IP, TCP_PORT):
    print 'Launching TCP Server...'
    TCP_PORT = int(TCP_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

    print 'Server Launched!'
    print 'Waiting for clients...'
    i = 0

    while True:
        i = i + 1
        conn, addr = s.accept()
        print 'Connection started, from: ', addr
        thread.start_new_thread(newClient, (conn, addr, i))
    s.close()

def UDP_SOCKET(UDP_IP, UDP_PORT):
    print 'Launching UDP Server...'
    UDP_PORT = int(UDP_PORT)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (UDP_IP, UDP_PORT)
    udp.bind(orig)

    print 'Server Launched!'
    print 'Waiting for clients...'

    i = 0
    while True:
        i = i + 1
        stringData, client = udp.recvfrom(409600)
        print 'Connection started, from: ', client
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg = cv2.imdecode(data, 1)
        checkFace = faceRecognition(decimg, i)
        if checkFace == 1:
            cv2.imwrite('received ' + str(i) + '.jpg', decimg)
    udp.close()

def faceRecognition(image, i):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) >= 1:
        print 'Face found on image: ', i
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        return 1

    else:
        print 'Face not found on image: ', i
        return 0


#TCP_IP = '192.168.100.103'
#TCP_IP = '127.0.0.1'
#TCP_PORT = 4040

IP = raw_input('Server IP Address: ')
PORT = raw_input('Server Port: ')

print 'Choose server protocol: '
print '1 - TCP Server;'
print '2 - UDP Server;'
serverType = raw_input('Option: ')
if serverType == '1':
    print 'TCP Server Init...'
    TCP_SOCKET(IP, PORT)

elif serverType == '2':
    print 'UDP Server Init...'
    UDP_SOCKET(IP, PORT)
else:
    print 'Invalid Option.'

