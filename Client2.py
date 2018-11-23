import socket
import cv2
import numpy

TCP_IP = '192.168.100.109'
TCP_PORT = 4040

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

frame = cv2.imread('Foto.jpg')

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
result, imgencode = cv2.imencode('.jpg', frame, encode_param)
data = numpy.array(imgencode)
stringData = data.tostring()

sock.send(str(len(stringData)).ljust(16))
sock.send(stringData)
sock.close()
