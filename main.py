import curses
import sys
import multiprocessing

from sneeze.screen import Screen
from sneeze.logging import Logger
from proxy.proxy import Proxy

class ProxyHandler:
    def __init__(self, http_log): 
        self.proxy = Proxy('127.0.0.1', 4949, http_log)

    def start_proxy(self):
        self.proxy.listen()

    def kill(self):
        self.proxy.listening = False

def run(screen, http_log):
    ph = ProxyHandler(http_log)
   
    t1 = multiprocessing.Process(target=screen.run, args=(http_log,))
    t2 = multiprocessing.Process(target=ph.start_proxy)

    t1.start()
    t2.start()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        http_log = Logger(sys.argv[1])
    else:
        print('USAGE\npython3 sneeze.py <path/to/config/file>')
        exit()
    screen = Screen()

    run(screen, http_log)
