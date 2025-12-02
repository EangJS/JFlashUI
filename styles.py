from PyQt6.QtWidgets import (QPushButton, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt

class MaterialButton(QPushButton):
    def __init__(self, text="", parent=None, kind="default"):
        super().__init__(text, parent)

        # Set cursor to pointing hand
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Kind determines color scheme
        self.kind = kind

        # Apply initial style
        self.update_style()

    def update_style(self):
        if self.kind == "default":
            bg = "#33334c"
            hover = "#666698"
            pressed = "#9999e4"
            text_color = "#ffffff"
        elif self.kind == "danger":
            bg = "#e74c3c"
            hover = "#ff5252"
            pressed = "#c0392b"
            text_color = "#ffffff"
        elif self.kind == "success":
            bg = "#27ae60"
            hover = "#2ecc71"
            pressed = "#1e8449"
            text_color = "#ffffff"
        else:
            bg = "#33334c"
            hover = "#666698"
            pressed = "#9999e4"
            text_color = "#ffffff"

        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {text_color};
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {hover};
            }}
            QPushButton:pressed {{
                background: {pressed};
            }}
        """)
    
class MaterialCheckBox(QCheckBox):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        

class MaterialComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QComboBox {
                background: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px;
            }
            QComboBox:hover {
                border: 1px solid #1f6feb;
            }
            QComboBox::drop-down {
                background: transparent;
                border: none;
                width: 28px;
            }
            QComboBox::down-arrow {
                image: url("assets/arrow_drop_down.svg");
                width: 14px;
                height: 14px;
            }
            QComboBox QAbstractItemView {
                background: #1e1e1e;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 4px;
                outline: 0;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 10px;
                background: transparent;
                color: #e0e0e0;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #2a2a2a;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:selected {
                background: #1f6feb;
                color: white;
                border-radius: 4px;
            }
        """)
