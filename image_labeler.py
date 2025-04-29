import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QListWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from widgets.image_viewer import ImageViewer
from file_utils import (get_image_paths, save_label)

class ImageLabeler(QWidget):
    def __init__(self, initial_folder=None):
        super().__init__()
        self.setWindowTitle("Image Labeler (Qt)")
        self.image_dir = ""
        self.image_paths = []
        self.current_index = -1

        self.init_ui()

        if initial_folder:
            self.load_images_from_folder(initial_folder)

    def init_ui(self):
        layout = QHBoxLayout()

    # === LEFT SIDEBAR ===
        sidebar_layout = QVBoxLayout()

        load_button = QPushButton("Open Folder")
        load_button.clicked.connect(self.open_folder)
        sidebar_layout.addWidget(load_button)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.load_image)
        sidebar_layout.addWidget(self.list_widget)

        layout.addLayout(sidebar_layout, 2)

    # === RIGHT PANEL (Image + Label) ===
        right_panel = QVBoxLayout()

        self.image_label = ImageViewer("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.wheelScrolled.connect(self.scroll_image)
        right_panel.addWidget(self.image_label)

        self.label_input = QTextEdit()
        self.label_input.setPlaceholderText("Enter label here...")
        self.label_input.setMinimumHeight(70) 
        self.label_input.setFontPointSize(14)
        self.label_input.setLineWrapMode(QTextEdit.WidgetWidth)
        self.label_input.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        right_panel.addWidget(self.label_input)

        self.save_button = QPushButton("Save Label")
        self.save_button.clicked.connect(self.save_label)
        right_panel.addWidget(self.save_button)

        layout.addLayout(right_panel, 8)
        self.setLayout(layout)

   
    def load_images_from_folder(self, folder):
        self.image_paths = get_image_paths(folder)
        self.list_widget.clear()
        for path in self.image_paths:
            self.list_widget.addItem(os.path.basename(path))

        if self.image_paths:
            self.current_index = 0
            self.list_widget.setCurrentRow(0)
            self.load_image(0)
        else:
            QMessageBox.information(self, "No Images", "No .jpg or .png images found.")

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if not folder:
            return
        self.load_images_from_folder(folder)

    def load_image(self, index):
        if index < 0 or index >= len(self.image_paths):
            return

        self.current_index = index
        image_path = self.image_paths[index]

        # Load image
        pil_image = Image.open(image_path)
        pil_image.thumbnail((800, 600))
        qt_image = QPixmap(image_path)
        self.image_label.setPixmap(qt_image.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Load label
        label_path = os.path.splitext(image_path)[0] + ".txt"
        if os.path.exists(label_path):
            with open(label_path, "r", encoding="utf-8") as f:
                self.label_input.setPlainText(f.read())
        else:
            self.label_input.clear()

    def save_label(self):
        if self.current_index < 0:
            return

        image_path = self.image_paths[self.current_index]
        save_label(image_path, self.label_input)

    def scroll_image(self, direction):
        new_index = self.current_index + direction
        if 0 <= new_index < len(self.image_paths):
            self.current_index = new_index
            self.list_widget.setCurrentRow(self.current_index)
