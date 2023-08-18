import sys

from widgets import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery = MainDialog()
    gallery.show()
    sys.exit(app.exec())
