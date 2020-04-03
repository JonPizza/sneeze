import curses
import os

def handle_keystroke(action, screen, http_log):
    if action.lower() == 'e':
        editor = http_log.config['editor']['editor']
        screen.stop()
        os.system(f'{editor} {http_log.config_file}')
        screen.run(http_log)


def edit_positions(screen, action, http_log):
    screen.bottom_msg = '<e> - Edit | <l> - Launch | <p> - Switch Pos/Pay | Fuzzing on %FUZZ%'
    stdscr = screen.stdscr 
    
    height, width = stdscr.getmaxyx()
    handle_keystroke(action, screen, http_log)

    y = 4
    for line in screen.attacking_req.rstrip().split('\n'):
        try:
            stdscr.addstr(y, 1, trunc(line, width))
        except:
            stdscr.addstr(y - 2, 1, '-- TRUNCATED --')
            break
        y += 1

