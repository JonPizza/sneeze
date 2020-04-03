from proxy.proxy import Request, Response
import configparser
import time

class Logger:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        
        self.save_file = self.config['save']['save_file']
        
        self.token1 = '\n.vy5Qk++8Mkslq*.N}bwtHfH4eCNxU;VL_#s"2L7RR7RJA+!T"&#MAb~y<ry 3$WSMc0=g$QXHw`6H<OwF0cY)_v<k+gb-rKT&\n'
        self.token2 = '\nzvc0=g$QXHw`66H<O---y-u-look-@-dis-code??--------"&#MAb~y<ry.3$mmmmmmmmAjs#@I(eifd++Y)redditfunny&\n'


    def append_req_res(self, req, res):
        with open(self.save_file, 'a') as f:
            f.write(req + self.token2 + res + self.token1)
    
    def clear(self):
        with open(self.save_file, 'w') as f:
            f.write('')

    def shorten(self, max_pairs=50):
        log = self.read()
        if len(log) >= max_pairs:
            self.clear()
            for i in range(0, max_pairs)[::-1]:
                self.append_req_res(log[i]['req'], log[i]['res'])
    
    def reload_config(self):
        self.config.read(self.config_file)

    def read(self):
        req_and_res = []
        with open(self.save_file) as f:
            for r in f.read().split(self.token1):
                if r == '':
                    continue
                r = r.split(self.token2)

                req_and_res.append({
                    'req': Request(r[0]),
                    'res': Response(r[1]),
                })
        return req_and_res
