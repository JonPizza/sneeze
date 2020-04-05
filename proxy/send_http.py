from requests import Request, Session
from .http_classes import Request as RequestParser

def as_str(res):
    head = f'HTTP/1.1 {res.status_code} {res.raw.reason}'
    for key, val in res.headers.items():
        head += f'\r\n{key}: {val}'
    return head + '\r\n\r\n' + res.text

def set_headers(r, headers):
    r = r.prepare()
    
    for h in ['Host', 'User-Agent', 'Accept-Encoding', 'Accept']:
        if h in r.headers:
            del r.headers[h]

    for key, val in headers.items():
        r.headers[key] = val

    return r

def send_http_req(req):
    req = RequestParser(req)
    s = Session()
    r = Request(req.method, req.url, data=req.body)
    r = set_headers(r, req.headers)
    return as_str(s.send(r))
