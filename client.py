import numpy as np
import socket
import cv2


HOST = '192.168.100.109'
PORT = 4040

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

image = cv2.imread("Foto.jpg")

try:
    imgArray = np.array(image)
    imgLen = len(imgArray)
    sock.sendall("Tamanho %s" %imgLen)
    serverAnswer = sock.recv(4096)
    print 'Resposta: %s' %serverAnswer
    if serverAnswer == 'Size R':
        sendImg = imgArray.tostring()
        sock.sendall(sendImg)
        serverAnswer = sock.recv(4096)
        print 'Resposta: %s' %serverAnswer
        if serverAnswer == 'Imagem R':
            sock.sendall("Over")
            print 'Imagem enviada!'

finally:
    sock.close()
