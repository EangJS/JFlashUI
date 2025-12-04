from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout
from styles import MaterialButton, MaterialCheckBox

class FlashFileWidget(QWidget):
    """
    A widget to select a file to flash, with address input and enable checkbox,
    and hex viewer integration.
    """
    def __init__(self, label_text, default_address, file_filter="(*.bin *.trpk)"):
        super().__init__()

        self.file_path = QLineEdit()
        self.addr = QLineEdit(default_address)
        self.addr.setMaximumWidth(100)
        self.chk_enable = MaterialCheckBox()
        self.chk_enable.setChecked(False)

        self.btn_browse = MaterialButton("Browse")
        self.file_filter = file_filter
        self.label_text = label_text

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(self.label_text)
        label.setMinimumWidth(150)

        layout.addWidget(label)
        layout.addWidget(self.file_path)
        layout.addWidget(self.addr)
        layout.addWidget(self.chk_enable)
        layout.addWidget(self.btn_browse)
        self.setLayout(layout)

        # Connect buttons
        self.btn_browse.clicked.connect(self.select_file)
        # Connect double-click on file_path to open hex viewer
        self.file_path.mouseDoubleClickEvent = self._on_file_double_click

    def _on_file_double_click(self, event):
        """
        Handle double-click on file_path QLineEdit to open hex viewer
        """
        self.open_hex_viewer()

    def select_file(self):
        from PyQt6.QtWidgets import QFileDialog
        file, _ = QFileDialog.getOpenFileName(self, f"Select {self.label_text}", "", self.file_filter)
        if file:
            self.file_path.setText(file)
            default_kernel_address = "08080000" if self.file_path.text().endswith(".trpk") else "08014000"
            default_bootloader_address = "08000000"
            is_bootloader = True if "boot" in self.file_path.text() else False
            self.addr.setText(default_bootloader_address if is_bootloader else default_kernel_address)
            self.chk_enable.setChecked(True)


    def open_hex_viewer(self):
        if not self.file_path.text():
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No file", "Please select a file first.")
            return

        from hex_viewer import Hexviewer
        self.viewer = Hexviewer(self.file_path.text())  # store as attribute to keep it alive
        try:
            with open(self.viewer.file_path, "rb") as f:
                self.viewer.data = bytearray(f.read())
            self.viewer.update_display()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to open file in hex viewer:\n{e}")
            return

        self.viewer.setWindowTitle(f"Hex viewer - {self.file_path.text()}")
        self.viewer.show()
        self.viewer.raise_()
        self.viewer.activateWindow()

    def get_file_info(self):
        return self.file_path.text().strip(), self.addr.text().strip(), self.chk_enable.isChecked()
