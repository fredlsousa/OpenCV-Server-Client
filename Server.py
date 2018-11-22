import socket, select
import numpy as np
import cv2

imgName = "image%s.jpg"

HOST = '192.168.100.107'
PORT = 4040


connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(True)

connected_clients_sockets.append(server_socket)

while True:
    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
    for sock in read_sockets:
        if sock == server_socket:
            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

        else:
            try:
                data = sock.recv(4096)
                txt = str(data)
                if data:
                    if data.startswith('Tamanho'):
                        tmp = txt.split()
                        size = int(tmp[1])
                        print('Tamanho recebido %s' %size)
                        sock.sendall('Size R')
                        stringReceived = sock.recv(size)
                        if stringReceived:
                            sock.sendall('Imagem R')
                            imgFinal = np.fromstring(stringReceived, dtype = 'uint8')
                            ans = sock.recv(4096)
                            print('Answer to received: %s' %ans)
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue

server_socket.close()







