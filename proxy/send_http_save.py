import socket
import gzip
from .http_classes import Request

def get_port_from_url(url):
    if url.startswith('http://'):
        return 80
    else:
        return 443


def get_host_and_port(req):
    if ':' in req.host:
        (host, port) = req.host.split(':')
    else:
        host = req.host
        port = get_port_from_url(req.url)
    return host, port


def recvall(sock):
    BUFF_SIZE = 256 
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data


def send_http_req(req):
    req = Request(req)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    (host, port) = get_host_and_port(req)
    s.connect((host, port))
    s.sendall(req.as_str.encode())
    recved = recvall(s)
    s.close()
    return gunzip_res(recved)

def gunzip_res(res):
    print(res)
    headers = res.split(b'\r\n\r\n')[0]
    body = b'\r\n\r\n'.join(res.split(b'\r\n\r\n')[1:])
    return headers + b'\r\n\r\n' + gzip.decompress(body)


