from PyQt5.QtWidgets import QTextEdit

class LabelEditor(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText("Enter label here...")
        self.setMinimumHeight(70)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setVerticalScrollBarPolicy(self.ScrollBarAsNeeded)
