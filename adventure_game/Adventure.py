# File: Adventure.py
# ------------------
# This program plays the CS 106AX Adventure game.

from AdvGame import AdvGame
from pgl import *

# Constants
ADVENTURE_PREFIX = "Crowther"

# Main program
def Adventure():
    game = AdvGame(ADVENTURE_PREFIX)
    game.run()

def BlueRectangle():
    gw = GWindow(500, 300)
    rect = GRect(150, 50, 200, 100)
    rect.set_color("Blue")
    rect.set_filled(True)
    gw.add(rect)

# Startup code
if __name__ == "__main__":
    Adventure()
