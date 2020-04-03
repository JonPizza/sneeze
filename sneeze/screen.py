import curses
from curses import wrapper
import time

from .history import history
from .edit_settings import edit_settings
from .edit_http import edit_req, edit_res

class Screen:
    def __init__(self):
        self.tabs = ['Proxy', 'Editor', 'Attacker']
        self.selected_tab = 0
        self.sub_tabs = {
            'Proxy': ['History', 'Settings'],
            'Editor': ['Request', 'Response'],
            'Attacker': ['Payloads', 'Positions'],
        }
        self.selected_sub_tab = 0
        self.selected_row = 1
        self.window = 0
        self.running = True
        self.main_funcs = {
                'History': history,
                'Settings': edit_settings,
                'Request': edit_req,
                'Response': edit_res,
        }
        self.selected_req = 0
        self.editing_req_num = 0
        self.editing_req = ''
        self.editing_res = ''
        self.attacking_req = ''
        self.bottom_msg = 'Welcome to Sneeze!'

    def setup(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self.colors = {
            'highlight': curses.color_pair(1),
            'invert': curses.color_pair(2),
            'normal': curses.color_pair(3),
            'selected': curses.color_pair(4),
        }

        curses.curs_set(0)

    def draw(self, stdscr):
        self.stdscr = stdscr
        
        height, width = stdscr.getmaxyx()
        
        self.clear(height, width)
        self.setup()
        while True:
            if not self.running:
                break

            height, width = stdscr.getmaxyx()
            self.clear_window1(height, width)
            
            main = self.main_funcs[self.sub_tabs[self.tabs[self.selected_tab % len(self.sub_tabs)]][self.selected_sub_tab % 2]]
            main(self, '', self.log)

            self.draw_banner(width)
            if self.window == 0:
                self.bottom_msg = '<space> - Switch windows | <arrow keys> - Switch tabs'
            self.draw_bottom_msg(height, width)
            self.draw_tabs(self.tabs, self.selected_tab, 1, width)
            self.draw_tabs(self.sub_tabs[self.tabs[self.selected_tab % len(self.sub_tabs)]], self.selected_sub_tab, 2, width)
            self.draw_seperator(width, 3)

            action = stdscr.getkey()
            self.handle_tab_movement(action)

            if self.window == 1:
                main(self, action, self.log)
            
            stdscr.refresh()

    def clear_window1(self, height, width):
        for i in range(4, height - 1):
            self.stdscr.addstr(i, 0, ' ' * width)
        self.stdscr.addstr(height - 1, 0, ' ' * (width - 1))

    def clear(self, height, width):
        for i in range(height - 1):
            self.stdscr.addstr(i, 0, ' ' * width)

    def draw_banner(self, width):
        self.stdscr.addstr(0, 0, ' Sneeze v1.0.0' + ' ' * (width - 26) + 'By JonPizza ', self.colors['highlight'])

    def draw_bottom_msg(self, height, width):
        self.stdscr.addstr(height - 1, 0, ' ' + self.bottom_msg + ' ' * (width - len(self.bottom_msg) - 2), self.colors['invert'])

    def handle_tab_movement(self, action):
        if action == ' ':
            if self.window == 1:
                self.window = 0
            else:
                self.window = 1
        
        if self.window == 1:
            return

        if action == 'KEY_RIGHT':
            if self.selected_row == 1:
                self.selected_tab += 1
            else:
                self.selected_sub_tab += 1

        elif action == 'KEY_LEFT':
            if self.selected_row == 1:
                self.selected_tab -= 1
            else:
                self.selected_sub_tab -= 1
        
        elif action == 'KEY_DOWN':
            if self.selected_row == 1:
                self.selected_row = 2
        
        elif action == 'KEY_UP':
            if self.selected_row == 2:
                self.selected_row = 1

    def draw_tabs(self, tabs, selected, y, width):
        self.stdscr.addstr(y, 0, ' ' * width)

        x = 2

        if 1 == self.window:
            self.stdscr.addstr(1, 0, '▼')
            self.stdscr.addstr(2, 0, '▼')
        elif 1 == self.selected_row:
            self.stdscr.addstr(1, 0, '➞')
            self.stdscr.addstr(2, 0, ' ')
        else:
            self.stdscr.addstr(2, 0, '➞')
            self.stdscr.addstr(1, 0, ' ')

        for tab in tabs:
            if tab != tabs[abs(selected) % len(tabs)]:
                self.stdscr.addstr(y, x, f' {tab} ', self.colors['invert'])
            else:
                self.stdscr.addstr(y, x, f' {tab} ', self.colors['selected'])
            x += len(tab) + 4
    
    def draw_seperator(self, width, y):
        self.stdscr.addstr(y, 0, '«' * width)

    def stop(self):
        self.running = False
        curses.endwin()

    def run(self, log):
        self.log = log
        self.running = True

        wrapper(self.draw)

if __name__ == '__main__':
    screen = Screen()
    screen.run()
