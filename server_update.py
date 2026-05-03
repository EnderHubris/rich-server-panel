from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from display_panel import ServerList

from time import sleep
import threading

class Spinner:
    def __init__(self, description="Working..."):
        self._description = description
        self._stop = threading.Event()
        self._thread = None

    def _run(self):
        with Progress(SpinnerColumn(), TextColumn("{task.description}")) as p:
            p.add_task(self._description, total=None)  # total=None = infinite
            while not self._stop.is_set():
                sleep(0.1)

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

server_panel = ServerList()
console = Console()

def render_panel():
    global server_panel
    global console

    display = server_panel.print()
    console.print(Panel(display, title="Server Interface", subtitle="Select - Arrows    Quit - Q/Esc   Select - Enter"))

# use native systems file_descriptors to extract stdin input
import sys, tty, termios

KEY_UP    = '\x1b[A'
KEY_DOWN  = '\x1b[B'
KEY_LEFT  = '\x1b[D'
KEY_RIGHT = '\x1b[C'
KEY_ENTER = '\r'
KEY_ESC   = '\x1b'
KEY_SPACE = ' '

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)  # read rest of escape sequence
        return ch
    finally:
        # restore previous stdin fd state
        # works even on a crash
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def interact():
    global server_panel
    global console

    while True:
        console.clear()

        render_panel()
        key = get_key()

        if key == KEY_UP:
            server_panel.prev_selection()
            render_panel()
        elif key == KEY_DOWN:
            server_panel.next_selection()
            render_panel()

        elif key == KEY_ENTER:
            console.clear()

            spinner = Spinner("Creating backup...")
            spinner.start()
            status, msg = server_panel.perform()
            spinner.stop()

            console.clear()

            if status:
                console.print(f"[green italic]{msg}")
            else:
                console.print(f"[red bold]{msg}")
            sleep(3)

        elif key == KEY_ESC or key == 'q':
            break;
    console.clear()

def main():
    interact()

if __name__ == "__main__":
    main()
