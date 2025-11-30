import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QPlainTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from theme import hex_box_style

class Hexviewer(QWidget):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("Hex viewer")
        self.resize(900, 600)
        self.file_path = file_path
        self.data = bytearray()

        self.init_ui()

    def init_ui(self):

        viewer_layout = QHBoxLayout()

        # ---------------- Hex Display ----------------
        self.hex_box = QPlainTextEdit()
        self.hex_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.hex_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.hex_box.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.hex_box.setReadOnly(True)

        # ASCII display
        self.ascii_box = QPlainTextEdit()
        self.ascii_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.ascii_box.setReadOnly(True)

        viewer_layout.addWidget(self.hex_box, 3)
        viewer_layout.addWidget(self.ascii_box, 1)

        # Style for dark theme and visible scrollbar handle
        self.hex_box.setStyleSheet(hex_box_style())
        self.ascii_box.setStyleSheet(hex_box_style())

        # Disable vertical scrollbar on ASCII box
        self.ascii_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Sync ASCII box scroll with hex box
        self.hex_box.verticalScrollBar().valueChanged.connect(
            lambda value: self.ascii_box.verticalScrollBar().setValue(value)
        )

        self.setLayout(viewer_layout)


    def save_file(self):
        hex_text = self.hex_box.toPlainText().replace(" ", "").replace("\n", "")
        if not self.file_path:
            return
        try:
            self.data = bytearray.fromhex(hex_text)
            with open(self.file_path, "wb") as f:
                f.write(self.data)
            QMessageBox.information(self, "Saved", "File saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    # ---------------- Display and Editing ----------------
    def update_display(self):
        """Regenerate hex + ASCII display"""
        lines = []
        ascii_lines = []
        for i in range(0, len(self.data), 16):
            chunk = self.data[i:i+16]
            hex_bytes = " ".join(f"{b:02X}" for b in chunk).ljust(47)
            ascii_bytes = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            lines.append(f"{i:08X}  {hex_bytes}")
            ascii_lines.append(f"{ascii_bytes}")

        self.hex_box.blockSignals(True)
        self.hex_box.setPlainText("\n".join(lines))
        self.hex_box.blockSignals(False)

        self.ascii_box.blockSignals(True)
        self.ascii_box.setPlainText("\n".join(ascii_lines))
        self.ascii_box.blockSignals(False)

def main():
    app = QApplication(sys.argv)
    viewer = Hexviewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
