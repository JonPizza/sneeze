import socket

def get_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

def get_tls_data(host, port, data):
    print('yo')
    sock = get_socket(host, port)
    sock.send(data)
    recved = recvall(sock)
    print(recved) 
    return recved 
