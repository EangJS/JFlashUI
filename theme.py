def get_theme():
    style_sheet = """
        /* ----- GLOBAL ----- */

        /* Overrides for QComboBox to match dark theme */
        QComboBox, 
        /* ----- COMBOBOX (Dropdown) ----- */
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

        /* prevent it from looking like a button */
        QComboBox::drop-down {
            background: transparent;
            border: none;
            width: 28px;
        }

        /* custom svg arrow */
        QComboBox::down-arrow {
            image: url("assets/arrow_drop_down.svg");
            width: 14px;
            height: 14px;
        }

        /* popup menu */
        QComboBox QAbstractItemView {
            background: #1e1e1e;
            border: 1px solid #3a3a3a;
            selection-background-color: #1f6feb;
            selection-color: white;
            outline: none;
        }

        /* scrollbar in dropdown */
        QComboBox QScrollBar:vertical {
            background: #1e1e1e;
            width: 10px;
        }
        QComboBox QScrollBar::handle:vertical {
            background: #3a3a3a;
            border-radius: 5px;
        }
        QComboBox QScrollBar::handle:vertical:hover {
            background: #555;
        }

        /* ---------- DROPDOWN POPUP (the list) ---------- */

        /* The popup container */
        QComboBox QAbstractItemView {
            background: #1e1e1e;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            padding: 4px;
            outline: 0;
        }

        /* Each item inside the dropdown */
        QComboBox QAbstractItemView::item {
            padding: 6px 10px;
            background: transparent;
            color: #e0e0e0;
        }

        /* Hover highlight */
        QComboBox QAbstractItemView::item:hover {
            background: #2a2a2a;
            border-radius: 4px;
        }

        /* Selected item highlight */
        QComboBox QAbstractItemView::item:selected {
            background: #1f6feb;
            color: white;
            border-radius: 4px;
        }

        QWidget {
            font-family: Segoe UI, Arial;
            font-size: 12pt;
            background: #1e1d2b;
            color: #e0e0e0;
        }

        QLabel {
            color: #e0e0e0;
            font-weight: 500;
        }

        /* ----- INPUT FIELDS ----- */
        QLineEdit {
            background: #1e1e1e;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            padding: 6px;
            color: #ffffff;
        }
        QLineEdit:focus {
            border: 1px solid #1f6feb;
            background: #1a1a1a;
        }

        QTextEdit {
            background: #1e1e1e;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            padding: 6px;
            color: #e0e0e0;
        }

        /* ----- SCROLLBARS ----- */
        QScrollBar:vertical {
            background: #2a2a3d;
            width: 14px;
            margin: 0px 0px 0px 0px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical {
            background: #6c6cff;
            min-height: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            background: #2a2a3d;
            height: 14px;
            margin: 0px 0px 0px 0px;
            border-radius: 4px;
        }

        QScrollBar::handle:horizontal {
            background: #6c6cff;
            min-width: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }

        /* Red “danger” buttons */
        QPushButton[role="danger"] {
            background: #e74c3c;  /* red */
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: bold;
        }

        QPushButton[role="danger"]:hover {
            background: #ff5252;
        }

        QPushButton[role="danger"]:pressed {
            background: #c0392b;
        }

        QCheckBox {
            spacing: 10px;  /* space between box and label */
            color: #e0e0e0;
            font-weight: 500;
        }

        /* Box (indicator) */
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 4px;   /* rounded edges */
            border: 2px solid #555555;
            background: #1e1e1e;
        }

        /* Checked state */
        QCheckBox::indicator:checked {
            background: #1f6feb;  /* Material blue */
            border: 2px solid #1f6feb;
        }

        /* Hover effect */
        QCheckBox::indicator:hover {
            border: 2px solid #2a7bf5;
        }

        /* Disabled state */
        QCheckBox::indicator:disabled {
            background: #2a2a2a;
            border: 2px solid #444444;
            color: #777777;
        }

        QCheckBox::indicator:checked {
            image: url("assets/check.svg");
            background: #1f6feb;
        }
    """
    return style_sheet


def hex_box_style():
    return """
    QPlainTextEdit {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: Courier New;
        font-size: 10pt;
    }

    QScrollBar:vertical {
        background: #2a2a3d;
        width: 14px;
        margin: 0px 0px 0px 0px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical {
        background: #6c6cff;
        min-height: 20px;
        border-radius: 4px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    QScrollBar:horizontal {
        background: #2a2a3d;
        height: 14px;
        margin: 0px 0px 0px 0px;
        border-radius: 4px;
    }

    QScrollBar::handle:horizontal {
        background: #6c6cff;
        min-width: 20px;
        border-radius: 4px;
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
    """