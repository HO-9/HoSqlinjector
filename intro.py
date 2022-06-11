from pyfiglet import Figlet
from termcolor import cprint

def print_logo():
    f = Figlet(font='banner3-D',justify="center")
    cprint('===============================================================================================', 'red')
    cprint(f.renderText('Brute SQL'),'yellow')
    cprint('======================================================================================Ver 1.0==', 'red')
