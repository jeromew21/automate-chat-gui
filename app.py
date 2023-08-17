import time
from typing import Tuple, Callable
from dataclasses import dataclass

from pynput import mouse, keyboard

@dataclass
class GuiData:
    """Class for obtained data from user about gui chat"""
    chat_name: str

class Gui:
    """Namespace for gui methods"""
    @staticmethod
    def block_for_mouse_down() -> Tuple[int, int]:
        def handler(x, y, button, pressed) -> bool:
            if button == mouse.Button.left or button == mouse.Button.right:
                print("left mouse haha")
                return False
            else:
                return True
        
        listener = mouse.Listener(on_click=handler)
        listener.start()
        listener.join()
        controller = mouse.Controller()
        print(controller.position)
        return controller.position
    
    @staticmethod
    def click_at_position(position: Tuple[int, int], delay=0.1):
        controller = mouse.Controller()
        controller.position = position
        time.sleep(delay)
        controller.click(mouse.Button.left)
    
    @staticmethod
    def type_characters(chars: str, delay_fn: Callable = lambda: 0):
        controller = keyboard.Controller()
        # controller.type(chars)
        for letter in chars:
            controller.press(letter)
            controller.release(letter)
            time.sleep(delay_fn())


    

# print("Click location of text box.")
# pos = Gui.block_for_mouse_down()
# time.sleep(1)
# Gui.click_at_position(pos, delay=0.1)
# Gui.type_characters("hello world", lambda: 0.1)

import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(220, 32),
                QtWidgets.qApp.desktop().availableGeometry()
        ))

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec_()