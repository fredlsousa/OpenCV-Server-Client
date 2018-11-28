import socket
import cv2
import numpy
import thread

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

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
TCP_IP = '127.0.0.1'
TCP_PORT = 4040

print 'Launching Server...'


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