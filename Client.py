import socket
import cv2
import numpy
import time


def TCP_SOCKET(TCP_IP, TCP_PORT, times):
    TCP_PORT = int(TCP_PORT)
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))


    for i in range(0, int(times)):
        for j in range(0, 9):
            frame = cv2.imread('Foto' + str(j) + '.jpg')
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
    buf = 1024
    startstamp = time.time()
    for i in range(0, int(times)):
        for j in range(0,9):
            f = open('Foto' + str(i) + '.jpg', "rb")
            data = f.read(buf)
            while (data):
                if (udp.sendto(data, dest)):
                    data = f.read(buf)
    f.close()
    udp.sendto("end image", dest)
    stopstamp = time.time()
    print 'Time: ', stopstamp - startstamp
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