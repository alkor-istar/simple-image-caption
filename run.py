import sys
from PyQt5.QtWidgets import QApplication
from image_labeler import ImageLabeler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    initial_folder = sys.argv[1] if len(sys.argv) > 1 else None
    window = ImageLabeler(initial_folder=initial_folder)
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())
