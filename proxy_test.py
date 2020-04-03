from sneeze.logging import Logger
from proxy.proxy import Proxy

if __name__ == '__main__':
    proxy = Proxy('127.0.0.1', 4949, Logger('sneeze.ini'))
    print('Proxy listening at 127.0.0.1:4949')
    proxy.listen()
