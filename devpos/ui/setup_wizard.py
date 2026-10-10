from __future__ import annotations

from pathlib import Path
from typing import Optional

from devpos.core.config import load_config, save_config

def open_setup_wizard() -> Optional[dict]:
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QDialog,
            QFormLayout,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QPushButton,
            QVBoxLayout,
            QFileDialog,
        )
    except ImportError as exc:
        raise RuntimeError("PySide6 is required for the setup wizard.") from exc

    app = QApplication.instance() or QApplication([])

    dialog = QDialog()
    dialog.setWindowTitle("POS Setup")

    company_name = QLineEdit("Dev Tribhoomi")
    display_name = QLineEdit("Dev Tribhoomi POS")
    internal_id = QLineEdit("devtribhoomi")
    tagline = QLineEdit("Khadhye Udhyog, Kathmandu")

    logo_path = QLineEdit("")
    logo_button = QPushButton("Choose Logo")
    def choose_logo():
        path, _ = QFileDialog.getOpenFileName(dialog, "Select Logo", "", "Images (*.png *.jpg *.jpeg *.svg)")
        if path:
            logo_path.setText(path)

    logo_button.clicked.connect(choose_logo)

    form = QFormLayout()
    form.addRow("Company name", company_name)
    form.addRow("Display name", display_name)
    form.addRow("Internal ID", internal_id)
    form.addRow("Tagline", tagline)
    form.addRow("Logo", logo_path)
    form.addRow("", logo_button)

    buttons = QHBoxLayout()
    ok = QPushButton("Save")
    cancel = QPushButton("Cancel")

    buttons.addStretch()
    buttons.addWidget(ok)
    buttons.addWidget(cancel)

    layout = QVBoxLayout()
    layout.addWidget(QLabel("Set up your POS company branding"))
    layout.addLayout(form)
    layout.addLayout(buttons)

    dialog.setLayout(layout)

    result = {}

    def save_and_close():
        nonlocal result
        config = load_config()

        config["company"]["name"] = company_name.text().strip() or "Dev Tribhoomi"
        config["company"]["display_name"] = display_name.text().strip() or "Dev Tribhoomi POS"
        config["company"]["internal_id"] = internal_id.text().strip() or "devtribhoomi"
        config["company"]["tagline"] = tagline.text().strip() or "Khadhye Udhyog, Kathmandu"
        config["company"]["logo_path"] = logo_path.text().strip()

        config["app"]["window_title"] = display_name.text().strip() or "Dev Tribhoomi POS"
        config["app"]["data_folder_name"] = f"{config['company']['internal_id'].replace(' ', '').title()}POS"
        config["app"]["practice_folder_name"] = f"{config['app']['data_folder_name']}-Practice"

        save_config(config)
        result = config
        dialog.accept()

    ok.clicked.connect(save_and_close)
    cancel.clicked.connect(dialog.reject)

    dialog.exec()

    return result if result else None
