import sys
import curses

def handle_keystroke(action, screen, http_log):
    if action == 'KEY_DOWN':
        screen.selected_req += 1
    elif action == 'KEY_UP':
        screen.selected_req -= 1
    elif action == 'e':
        screen.selected_tab = 1
        screen.selected_sub_tab = 0
        screen.editing_req_num = screen.selected_req
        height, width = screen.stdscr.getmaxyx()

        log = http_log.read()
        pair = log[::-1][screen.selected_req % len(log[:height - 7])]
        screen.editing_req = pair['req'].as_str
        screen.editing_res = pair['res'].as_str


def format_for_screen(req, res, width):
    trunc_url = req.url[:width - 22] + '...' if len(req.url) >= (width - 22) else req.url
    return f'{res.status_code}    ‖ ' + req.method + ' ' * (8 - len(req.method)) + ' ‖ ' + trunc_url


def history(screen, action, http_log):
    stdscr = screen.stdscr
    height, width = stdscr.getmaxyx()
    stdscr.addstr(4, 2, 'STATUS ‖ METHOD   ‖ URL')
    stdscr.addstr(5, 2, '=' * (width - 4))

    height, width = stdscr.getmaxyx()
    y = 6
    log = http_log.read()[::-1]
    log = log[:height - 7]
    
    screen.bottom_msg = f'{len(log)} Requests | <e> - Send to editor | <a> - Send to attacker'

    handle_keystroke(action, screen, http_log)

    for i, http_pair in enumerate(log):
        if i == abs(screen.selected_req % len(log)):
            stdscr.addstr(y, 0, '➞')
        else:
            stdscr.addstr(y, 0, ' ')
        stdscr.addstr(y, 2, format_for_screen(http_pair['req'], http_pair['res'], width))
        y += 1

