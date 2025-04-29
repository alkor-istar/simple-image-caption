import os

def get_image_paths(folder):
    return sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

def load_label(image_path):
    label_path = os.path.splitext(image_path)[0] + ".txt"
    if os.path.exists(label_path):
        with open(label_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_label(image_path, text):
    plain_text = text.toPlainText()
    label_path = os.path.splitext(image_path)[0] + ".txt"
    with open(label_path, "w", encoding="utf-8") as f:
        f.write(plain_text)