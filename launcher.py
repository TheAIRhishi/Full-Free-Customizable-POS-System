"""Entry point for the packaged Windows program (PyInstaller) and for `python launcher.py`."""
import os
import sys

from devpos.core.config import ensure_first_run
from devpos.ui.app import main

if __name__ == "__main__":
    ensure_first_run()
    # Optional: keep branding available globally to the app
    os.environ.setdefault("DEVPOS_COMPANY_NAME", "Dev Tribhoomi")
    os.environ.setdefault("DEVPOS_COMPANY_DISPLAY_NAME", "Dev Tribhoomi POS")
    sys.exit(main(sys.argv))
