import socket
import cv2
import numpy



def TCP_SOCKET(TCP_IP, TCP_PORT, times):
    TCP_PORT = int(TCP_PORT)
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    frame = cv2.imread('Foto1.jpg')
    for i in range(0, int(times)):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()

        sock.send(str(len(stringData)).ljust(16))
        sock.send(stringData)
    sock.close()


def UDP_SOCKET(UDP_IP, UDP_PORT, times):
    UDP_PORT = int(UDP_PORT)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (UDP_IP, UDP_PORT)

    frame = cv2.imread('Foto.jpg')

    for i in range(0, int(times)):
        print 'Sending image...'
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        udp.sendto(stringData, dest)
        print 'Image sent.'
    udp.close()


IP = raw_input('Server IP Address: ')
PORT = raw_input('Server Port: ')

print 'Choose client protocol: '
print '1 - TCP Client;'
print '2 - UDP Client;'
serverType = raw_input('Option: ')
if serverType == '1':
    print 'TCP Server Init...'
    times = raw_input('How many pictures will be send: ')
    TCP_SOCKET(IP, PORT, times)

elif serverType == '2':
    print 'UDP Server Init...'
    times = raw_input('How many pictures will be send: ')
    UDP_SOCKET(IP, PORT, times)
else:
    print 'Invalid Option.'