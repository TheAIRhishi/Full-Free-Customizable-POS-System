import json
import os
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.json"

def default_config() -> Dict[str, Any]:
    return {
        "company": {
            "name": "Dev Tribhoomi",
            "display_name": "Dev Tribhoomi POS",
            "tagline": "Khadhye Udhyog, Kathmandu",
            "internal_id": "devtribhoomi",
            "logo_path": "",
        },
        "app": {
            "window_title": "Dev Tribhoomi POS",
            "data_folder_name": "DevTribhoomiPOS",
            "practice_folder_name": "DevTribhoomiPOS-Practice",
            "db_name": "devpos.db",
        },
    }

def load_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    config_file = Path(config_path)
    if not config_file.exists():
        config = default_config()
        save_config(config, config_file)
        return config

    with open(config_file, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    merged = default_config()
    merged.update(data)

    # deep-merge company/app blocks
    for section in ("company", "app"):
        if section in data:
            merged[section].update(data[section])

    save_config(merged, config_file)
    return merged

def save_config(config: Dict[str, Any], config_path: str | Path = DEFAULT_CONFIG_PATH) -> None:
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

def ensure_first_run(config_path: str | Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    config = load_config(config_path)

    company = config.get("company", {})
    app = config.get("app", {})

    app_data_dir = Path(os.getenv("LOCALAPPDATA", str(Path.home())))
    company_dir = app_data_dir / app.get("data_folder_name", "DevTribhoomiPOS")
    company_dir.mkdir(parents=True, exist_ok=True)

    # set env vars for the entire live app
    os.environ["DEVPOS_COMPANY_NAME"] = company.get("name", "Dev Tribhoomi")
    os.environ["DEVPOS_COMPANY_DISPLAY_NAME"] = company.get("display_name", "Dev Tribhoomi POS")
    os.environ["DEVPOS_COMPANY_INTERNAL_ID"] = company.get("internal_id", "devtribhoomi")
    os.environ["DEVPOS_APP_DATA_DIR"] = str(company_dir)
    os.environ["DEVPOS_DB_PATH"] = str(company_dir / app.get("db_name", "devpos.db"))

    return config

def get_runtime_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    return load_config(config_path)
