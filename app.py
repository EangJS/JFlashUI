import sys
import os
import shutil
import subprocess
import json
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QFileDialog, QVBoxLayout, QTextEdit, QMessageBox, QHBoxLayout,
    QInputDialog, QGraphicsDropShadowEffect, QFrame, QCheckBox
)
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import QThread, pyqtSignal, QSize
from theme import get_theme, hex_box_style
from styles import MaterialButton, MaterialCheckBox, MaterialComboBox
from widgets import FlashFileWidget
from parser import get_config, set_config

SETTINGS_FILE = "settings.json"
swd_speeds = ["1", "5", "100", "500", "1000", "2000", "4000", "4800", "6000", "8000", "9600", "12000", "15000", "20000", "25000", "30000", "40000"]


class FlashWorker(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            subprocess.run(self.cmd)
        except Exception as e:
            self.output.emit(f"Exception: {e}")

        self.finished.emit()


class JFlashGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_path = SETTINGS_FILE
        self.profiles = []
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("JFlash Programming Tool")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ---------------- Profile Selection ----------------
        profile_row = QHBoxLayout()
        lbl_profile = QLabel("Profile:")
        lbl_profile.setMinimumWidth(150)

        self.profile_select = MaterialComboBox()
        self.profile_select.setMinimumWidth(200)
        self.profile_select.currentIndexChanged.connect(self.load_profile)

        self.btn_add_profile = MaterialButton()
        self.btn_add_profile.setIcon(QIcon("assets/add.svg"))
        self.btn_add_profile.setIconSize(QSize(20, 20))
        self.btn_add_profile.clicked.connect(self.add_profile)

        self.btn_delete_profile = MaterialButton("🗑 Delete", kind="danger")
        self.btn_delete_profile.setMinimumWidth(80)
        self.btn_delete_profile.clicked.connect(self.delete_profile)

        profile_row.addWidget(lbl_profile)
        profile_row.addWidget(self.profile_select)
        profile_row.addWidget(self.btn_add_profile)
        profile_row.addWidget(self.btn_delete_profile)
        main_layout.addLayout(profile_row)

        # ---------------- JFlash Project File ----------------
        prj_layout = QHBoxLayout()
        prj_label = QLabel("📁 JFlash Project File:")
        prj_label.setMinimumWidth(150)
        self.prj_path = QLineEdit()
        btn_prj = MaterialButton("Browse")
        btn_prj.clicked.connect(self.select_project)
        prj_layout.addWidget(prj_label)
        prj_layout.addWidget(self.prj_path)
        prj_layout.addWidget(btn_prj)
        main_layout.addLayout(prj_layout)

        # ---------------- JLink Serial ----------------
        misc_layout = QHBoxLayout()
        sn_layout = QHBoxLayout()
        sn_label = QLabel("🔌 JLink Serial:")
        self.jlink_sn = QLineEdit()
        swd_speed_label = QLabel("SWD Speed (KHz):")
        self.swd_speed = MaterialComboBox()
        self.swd_speed.setMinimumWidth(100)
        for speed in swd_speeds:
            self.swd_speed.addItem(f"{speed}")
        self.swd_speed.currentTextChanged.connect(self.on_swd_combo_change)
        
        sn_layout.addWidget(sn_label)
        sn_layout.addWidget(self.jlink_sn)
        sn_layout.addWidget(swd_speed_label)
        sn_layout.addWidget(self.swd_speed)

        # Right-aligned: checkbox
        self.chip_erase = MaterialCheckBox("Full Chip Erase")

        misc_layout.addLayout(sn_layout)
        misc_layout.addWidget(self.chip_erase)
        main_layout.addLayout(misc_layout)

        # ---------------- Flash File Widgets ----------------
        self.bootloader_widget = FlashFileWidget("⚙️ Bootloader", "0x08000000", "Bootloader (*.bin *.trpk)")
        self.kernel_widget = FlashFileWidget("💿 App Image", "08080000", "(*.bin *.trpk)")
        self.param_widget = FlashFileWidget("💿 Secondary Image", "083FE000", "(*.bin)")

        main_layout.addWidget(self.bootloader_widget)
        main_layout.addWidget(self.kernel_widget)
        main_layout.addWidget(self.param_widget)

        # ---------------- Action Buttons ----------------
        action_frame = QFrame()
        action_frame.setFrameShape(QFrame.Shape.NoFrame)
        action_frame.setStyleSheet("""
            QFrame {
                background-color: #26273b;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 120))
        action_frame.setGraphicsEffect(shadow)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        action_frame.setLayout(action_layout)

        btn_run = MaterialButton("⚡ Run Flash")
        btn_save = MaterialButton("💾 Save Settings", kind="secondary")
        action_layout.addWidget(btn_run)
        action_layout.addWidget(btn_save)

        btn_run.clicked.connect(self.run_flash)
        btn_save.clicked.connect(self.save_settings)
        main_layout.addWidget(action_frame)

        # ---------------- Output Box ----------------
        self.output_box = QTextEdit()
        self.output_box.setFontFamily("Courier New")
        self.output_box.setFontPointSize(10)
        self.output_box.setStyleSheet(hex_box_style())

        self.output_box.setReadOnly(True)
        main_layout.addWidget(self.output_box)

        self.setLayout(main_layout)

    # ------------------------------------------------------------
    # SETTINGS JSON
    # ------------------------------------------------------------
    def add_profile(self):
        name, ok = QInputDialog.getText(self, "New Profile", "Profile name:")
        if not ok or not name.strip():
            return

        new_profile = {
            "name": name,
            "project_file": "",
            "bootloader": "",
            "image_file": "",
            "param_file": "",
            "addr_bootloader": "08000000",
            "addr_image": "08080000",
            "addr_param": "083FE000",
            "jlink_sn": ""
        }

        self.profiles.append(new_profile)
        self.profile_select.addItem(name)
        self.profile_select.setCurrentIndex(len(self.profiles) - 1)

    def delete_profile(self):
        index = self.profile_select.currentIndex()
        if index < 0:
            return

        del self.profiles[index]
        self.profile_select.removeItem(index)

        # Save updated list
        with open(self.settings_path, "w") as f:
            json.dump({"profiles": self.profiles}, f, indent=4)

        if self.profiles:
            self.load_profile(0)

    def load_profile(self, index):
        if index < 0 or index >= len(self.profiles):
            return

        p = self.profiles[index]

        self.project_file = p.get("project_file", "")
        self.prj_path.setText(self.project_file)
        if self.project_file != "":
            self.swd_speed.setCurrentText(str(get_config(self.project_file, "JTAG", "Speed1")))  # Default 4000 kHz

        self.bootloader_widget.file_path.setText(p.get("bootloader", ""))
        self.kernel_widget.file_path.setText(p.get("image_file", ""))
        self.param_widget.file_path.setText(p.get("param_file", ""))

        self.bootloader_widget.addr.setText(p.get("addr_bootloader", "08000000"))
        self.kernel_widget.addr.setText(p.get("addr_image", "08080000"))
        self.param_widget.addr.setText(p.get("addr_param", "083FE000"))

        self.bootloader_widget.chk_enable.setChecked(p.get("bootloader_enabled", False))
        self.kernel_widget.chk_enable.setChecked(p.get("image_enabled", False))
        self.param_widget.chk_enable.setChecked(p.get("param_enabled", False))

        self.jlink_sn.setText(p.get("jlink_sn", ""))
        self.chip_erase.setChecked(p.get("chip_erase", False))

    def load_settings(self):
        if not os.path.exists(self.settings_path):
            # Initialize empty profiles file
            with open(self.settings_path, "w") as f:
                json.dump({"profiles": []}, f, indent=4)

        try:
            with open(self.settings_path, "r") as f:
                data = json.load(f)

            self.profiles = data.get("profiles", [])

            # Load profile names into the dropdown
            self.profile_select.clear()
            for p in self.profiles:
                self.profile_select.addItem(p.get("name", "Unnamed Profile"))

            if self.profiles:
                self.load_profile(0)

            self.output_box.append("Loaded settings.json\n")

        except Exception as e:
            self.output_box.append(f"Failed to load settings: {e}\n")


    def save_settings(self):
        index = self.profile_select.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Error", "No profile selected.")
            return

        # Update profile object
        self.profiles[index] = {
            "name": self.profile_select.currentText(),
            "project_file": self.prj_path.text().strip(),
            "bootloader": self.bootloader_widget.get_file_info()[0].strip(),
            "image_file": self.kernel_widget.get_file_info()[0].strip(),
            "param_file": self.param_widget.get_file_info()[0].strip(),
            "addr_bootloader": self.bootloader_widget.addr.text().strip(),
            "addr_image": self.kernel_widget.addr.text().strip(),
            "addr_param": self.param_widget.addr.text().strip(),
            "jlink_sn": self.jlink_sn.text().strip(),
            "bootloader_enabled": self.bootloader_widget.chk_enable.isChecked(),
            "image_enabled": self.kernel_widget.chk_enable.isChecked(),
            "param_enabled": self.param_widget.chk_enable.isChecked(),
            "chip_erase": self.chip_erase.isChecked()
        }

        with open(self.settings_path, "w") as f:
            json.dump({"profiles": self.profiles}, f, indent=4)

        self.output_box.append("Saved profile to settings.json\n")


    # ------------------------------------------------------------
    # FILE SELECTION
    # ------------------------------------------------------------
    def select_project(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Project File", "", "JFlash Project (*.jflash)")
        if file:
            self.prj_path.setText(file)

    # ------------------------------------------------------------
    # CONFIG SELECTION
    # ------------------------------------------------------------
    def on_swd_combo_change(self, text):
        set_config(self.project_file, "JTAG", "Speed1", text)

    # ------------------------------------------------------------
    # FLASH EXECUTION
    # ------------------------------------------------------------
    def run_flash(self):
        # Ensure JFlash is available in PATH
        if shutil.which("JFlash.exe") is None:
            QMessageBox.critical(
                self,
                "Error",
                "JFlash.exe not found in PATH.\nPlease add JFlash.exe to system PATH."
            )
            return

        jflash = "JFlash.exe"

        project = self.prj_path.text().strip()
        if not os.path.exists(project):
            QMessageBox.critical(self, "Error", "Project file path is invalid.")
            return

        # File list
        binaries = [
            self.bootloader_widget.get_file_info(),
            self.kernel_widget.get_file_info(),
            self.param_widget.get_file_info()
        ]
        binaries = [(f, a) for f, a, chk in binaries if chk]

        if not binaries and not self.chip_erase.isChecked():
            QMessageBox.critical(self, "Error", "No binaries selected to flash.")
            return

        # Validate paths
        for file_path, _ in binaries:
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Error", f"Binary file not found:\n{file_path}")
                return

        # Validate hex addresses
        for label, addr in [
            ("Bootloader", self.bootloader_widget.addr.text()),
            ("Kernel", self.kernel_widget.addr.text()),
            ("BootParam", self.param_widget.addr.text())
        ]:
            a = addr.strip()
            if len(a) != 8 or any(c not in "0123456789ABCDEFabcdef" for c in a):
                QMessageBox.critical(self, "Error", f"{label} address is invalid.\nMust be 8-digit hex.")
                return

        # Build command
        cmd = [jflash, "-openprj", project.replace("/", "\\")]
        sn = self.jlink_sn.text().strip()
        if sn:
            cmd.extend(["-usb", sn])

        if self.chip_erase.isChecked():
            cmd.append("-erasechip")

        for bin_file, addr in binaries:
            bin_file = bin_file.replace("/", "\\")

            # TRPK → BIN conversion
            if bin_file.endswith(".trpk"):
                new_file = os.path.splitext(bin_file)[0] + ".bin"
                if not os.path.exists(new_file):
                    shutil.copy2(bin_file, new_file)
                bin_file = new_file

            # Append command sequence
            cmd.extend([
                f"-open\"{bin_file}\",{addr}",
                "-auto"
            ])

        cmd.append("-exit")

        # Show command
        self.output_box.append("\nRunning Command:\n" + " ".join(cmd) + "\n")

        # Start worker thread
        start_time = time.time()
        self.worker = FlashWorker(cmd)
        self.worker.output.connect(self.output_box.append)
        self.worker.finished.connect(lambda: self.output_box.append(f"\n--- Finished in {time.time() - start_time:.2f} seconds ---\n"))
        self.worker.start()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(get_theme())
    window = JFlashGUI()
    app.setWindowIcon(QIcon('assets/thunder.ico'))
    window.resize(700, 650)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
