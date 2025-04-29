# image_viewer.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QWheelEvent

class ImageViewer(QLabel):
    wheelScrolled = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta > 0:
            self.wheelScrolled.emit(-1)  # Scroll up → previous image
        elif delta < 0:
            self.wheelScrolled.emit(1)   # Scroll down → next image
