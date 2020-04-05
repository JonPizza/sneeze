import socket
import threading
import requests
from .http_classes import *
from .tls import get_tls_data 
from .send_http import send_http_req

def dddres_as_str(res):
    str_res = f'HTTP/1.1 {res.status_code} {status_messages.get(res.status_code)}\n'
    for key, val in res.headers.items():
        if key.lower() == 'proxy-connection':
            continue
        str_res += f'{key}: {val}\n'
    str_res += '\n'
    str_res += res.text
    return str_res

def should_log(url, log):
    for ext in log.config['scope']['ignore_exts']:
        if url.endswith(ext):
            return False
    return True

def strip_headers(res):
    return '\r\n\r\n'.join(res.split('\r\n\r\n')[1:])

class Proxy:
    def __init__(self, host, port, log):    
        self.host = host
        self.port = port
        self.log = log
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listening = True

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client,address)).start()

    def listen_to_client(self, client, address):
        if not self.listening:
            exit()
        size = 1024
        while True:
            data = client.recv(size)
            try:
                data = data.decode()
            except UnicodeDecodeError:
                # is TLS encrypted
                tls_data = get_tls_data(self.tls_host, self.tls_port, data) 
                client.send(tls_data)
                client.close()
                return 0

            if data:
                req = Request(data)
                exit_code = self.forward_request_and_log(req, client, address)
                if exit_code == 0:
                    client.close()
                return 0
            else:
                raise Exception('Client disconnected')
    
    def log_request_and_response(self, req, res):
        self.log.append_req_res(req, res)

    def forward_request_and_log(self, req, conn, address):
        if req.method == 'CONNECT':
            self.tls_host, self.tls_port = req.url.split(':')
            self.tls_port = int(self.tls_port)
            conn.send(b'HTTP/1.1 200 Connection established\r\n\r\n')
            return 1 

        try:
            res = send_http_req(req.as_str)
        except Exception as e:
            conn.send(open('HTML/error.html').read().replace('%HOST%', req.host).replace('%ERROR%', str(e)).encode())
            return 0
        
        if should_log(req.url, self.log):
            self.log_request_and_response(req.as_str, res)
        print(res)
        if Response(res).status_code != 304:
            conn.send(strip_headers(res).encode())
        else:
            conn.send(res.encode())
        return 0



