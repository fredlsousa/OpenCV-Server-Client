import socket
import cv2
import numpy
import thread
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')     #Database to identify the faces
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')                      #Database to identify the eyes

def recvall(sock, count):                                           #cria um buffer para transmissao
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def newClient(clientsocket, addr, i):
    while True:
        length = recvall(clientsocket, 16)                          #tamanho da foto a ser recebida
        stringData = recvall(clientsocket, int(length))             #stringData recebe o valor em string da foto
        data = numpy.fromstring(stringData, dtype='uint8')          #conversao de srting para numpy array
        decimg = cv2.imdecode(data, 1)                              #decodificando o numpy array em imagem
        checkFace = faceRecognition(decimg, i)                      #checando as faces no metodo faceRecognition
        if checkFace == 1:                                          #se existir uma face na foto, armazena no hd do server
            cv2.imwrite('received ' + str(i) + '.jpg', decimg)
        else:
            cv2.imwrite('received ' + str(i) + '.jpg', decimg)
        i = i + 1
    clientsocket.close()                                            #fecha o socket de conexao


def TCP_SOCKET(TCP_IP, TCP_PORT):
    print 'Launching TCP Server...'
    TCP_PORT = int(TCP_PORT)                                    #cast da porta, tem que ser int
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #abrindo o socket TCP em sock.SOCK_STREAM
    s.bind((TCP_IP, TCP_PORT))                                  #setando o server no ip e na porta especificada
    s.listen(True)                                              #TCP server escuta a rede

    print 'Server Launched!'
    print 'Waiting for clients...'
    i = 0
    while True:
        conn, addr = s.accept()                                 #aceita a conexao
        print 'Connection started, from: ', addr
        thread.start_new_thread(newClient, (conn, addr, i))     #inicia a thread chamando o metodo newClient
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
    buf = 1024
    while True:
        bytes = 0
        f = open('preImg' + str(i) + '.jpg', "wb")
        startstamp = time.time()
        data, addr = udp.recvfrom(buf)
        print 'Connection started, from: ', addr
        while (data):
            f.write(data)
            udp.settimeout(20)
            endstamp = time.time()
            bytes += len(data)
            data, addr = udp.recvfrom(buf)
            if data == "end image":
                rate = (bytes / (endstamp - startstamp) * 8) / 1000
                print "freq (Hz) = 5   "   "|   bit rate (kbps) = ", int(rate)
                time.sleep(20)
                break
        f.close()
        decimg = cv2.imread('preImg' + str(i) + '.jpg')
        checkFace = faceRecognition(decimg, i)
        if checkFace == 1:  # se existir uma face na foto, armazena no hd do server
            # cv2.imwrite('C:\\Users\\Frederico\\Desktop\\RedesTp\\Face\\received ' + str(i) + '.jpg', decimg)
            print 'Face found.'
            cv2.imwrite('received ' + str(i) + '.jpg', decimg)

        else:
            # cv2.imwrite('C:\\Users\\Frederico\\Desktop\\RedesTp\\NoFace\\received ' + str(i) + '.jpg', decimg)
            print 'Face not found.'
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

