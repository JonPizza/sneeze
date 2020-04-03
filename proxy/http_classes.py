status_messages = {
    100: 'Continue',
    101: 'Switching Protocols',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Time-out',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Large',
    415: 'Unsupported Media Type',
    416: 'Requested range not satisfiable',
    417: 'Expectation Failed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Time-out',
    505: 'HTTP Version not supported',
}

class Request:
    def __init__(self, request):
        self.as_str = request
        request = self.parse_request(request)
        self.method = request['method']
        self.url = request['url']
        self.version = request['version']
        self.headers = request['headers']
        self.body = request['body']
        self.host = self.headers['Host']
        
    def parse_request(self, request):  
        req = request.replace('\r', '').split('\n\n')
        header = req[0].split('\n')
        body = '\n\n'.join(req[1:]) if len(req) > 2 else ''

        method, url, version = header[0].split(' ')
        
        headers = {}
        for param in header[1:]:
            pos = param.find(': ')
            key, val = param[:pos], param[pos+2:]
            headers.update({key: val})

        return {
            'method': method, 
            'url': url, 
            'version': version, 
            'headers': headers, 
            'body': body,
        }

class Response:
    def __init__(self, response):
        self.as_str = response
        response = self.parse_response(response)
        self.status_code = response['status_code']
        self.version = response['version']
        self.headers = response['headers']
        self.body = response['body']
        
    def parse_response(self, response):  
        req = response.replace('\r', '').split('\n\n')
        header = req[0].split('\n')
        body = '\n\n'.join(req[1:])

        version, status_code, msg = header[0].split(' ')
        status_code = int(status_code)

        msg = status_messages.get(status_code, '')
        
        headers = {}
        for param in header:
            pos = param.find(': ')
            key, val = param[:pos], param[pos+2:]
            headers.update({key: val})

        return {
            'status_code': status_code, 
            'version': version, 
            'headers': headers,
            'body': body,
        }