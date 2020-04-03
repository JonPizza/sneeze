import curses
import os
import requests

from proxy.proxy import res_as_str
from proxy.http_classes import Request, Response

def send_req(req):
    req = Request(req)
    url = req.url
    headers = req.headers
    try:
        if req.method == 'GET':
            response = requests.get(url, headers=headers)
        elif req.method == 'POST':
            response = requests.post(url, data=req.body, headers=headers)
        elif req.method == 'HEAD':
            response = requests.head(url, headers=headers)
        elif req.method == 'PUT':
            response = requests.put(url, data=req.body, headers=headers)
        elif req.method == 'OPTIONS':
            response = requests.options(url, headers=headers)
        elif req.method == 'PATCH':
            response = requests.patch(url, data=req.body, headers=headers)
    except Exception as e:
        return f'Sneeze error: {e}'
    return res_as_str(response)


def handle_keystroke(action, screen, http_log):
    if action.lower() == 'e':
        if os.name == 'nt':
            filename = '%TEMP%\ACHOOO'
        else:
            filename = '/tmp/ACHOOOO.html'

        editor = http_log.config['editor']['editor']
        with open(filename, 'w') as f:
            if screen.selected_sub_tab == 0:
                f.write(screen.editing_req)
            else:
                f.write(screen.editing_res)

        screen.stop()
        
        os.system(f'{editor} {filename}')
        with open(filename) as f:
            if screen.selected_sub_tab == 0:
                screen.editing_req = f.read()
        screen.run(http_log)

    elif action.lower() == 'r':
        screen.selected_sub_tab = int(not screen.selected_sub_tab)

    elif action.lower() == 's':
        height, width = screen.stdscr.getmaxyx()
        screen.bottom_msg = 'Sending...'
        screen.editing_res = send_req(screen.editing_req)
        screen.selected_sub_tab = 1
        

def trunc(line, width):
    return line[:width - 2] if len(line) > width - 2 else line

def edit_req(screen, action, http_log):
    screen.bottom_msg = '<e> - Edit | <r> - Switch Req/Res | <s> - Send'
    stdscr = screen.stdscr

    height, width = stdscr.getmaxyx()
    handle_keystroke(action, screen, http_log)

    y = 4
    for line in screen.editing_req.rstrip().split('\n'):
        try:
            stdscr.addstr(y, 1, trunc(line, width))
        except:
            stdscr.addstr(y - 2, 1, '-- TRUNCATED --')
            break
        y += 1


def edit_res(screen, action, http_log):
    stdscr = screen.stdscr

    height, width = stdscr.getmaxyx()
    handle_keystroke(action, screen, http_log)
    screen.bottom_msg = f'{len(screen.editing_res)} bytes | <e> - Edit | <r> - Switch Req/Res | <s> - Send'

    y = 4
    for line in screen.editing_res.split('\n'):
        try:
            stdscr.addstr(y, 1, trunc(line, width))
        except:
            stdscr.addstr(y - 2, 1, '-- TRUNCATED --' + ' ' * (width - 15))
            break
        y += 1

