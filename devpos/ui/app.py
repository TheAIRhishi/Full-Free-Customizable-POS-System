from devpos.core.config import get_runtime_config

config = get_runtime_config()
company_name = config["company"]["display_name"]

# Example: update the main window title
self.setWindowTitle(company_name)
