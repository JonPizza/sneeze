import curses
import os

def handle_keystroke(action, screen, http_log):
    if action.lower() == 'e':
        editor = http_log.config['editor']['editor']
        screen.stop()
        os.system(f'{editor} {http_log.config_file}')
        screen.run(http_log)

def edit_settings(screen, action, http_log):
    screen.bottom_msg = 'Press <e> to edit'
    stdscr = screen.stdscr 
    
    height, width = stdscr.getmaxyx()
    handle_keystroke(action, screen, http_log)
        
    stdscr.addstr(4, 2, 'Current settings:')
    y = 5
    
    for key, val in http_log.config.items():
        if key == 'DEFAULT':
            continue
        try:
            stdscr.addstr(y, 2, f'\t{key}:')
            y += 1
            for key2, val2 in val.items():
                stdscr.addstr(y, 2, f'\t\t{key2}: {val2}')
                y += 1
        except:
            stdscr.addstr(y - 2, 1, '-- TRUCATED --' + ' ' * (width - 16))
            break
