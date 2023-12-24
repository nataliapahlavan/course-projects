from pgl import *

def BlueRectangle():
    gw = GWindow(500, 300)
    rect = GRect(150, 50, 200, 100)
    image = GImage("OutsideBuilding.png")
    rect.set_color("Blue")
    rect.set_filled(True)
    gw.add(image, 0, 0)

if __name__ == "__main__":
    BlueRectangle()
