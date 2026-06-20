from pathlib import Path
import json


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"

APP_SETTINGS_PATH = CONFIG_DIR / "app_settings.json"
CAPTURE_REGION_PATH = CONFIG_DIR / "capture_region.json"
OBJECTS_PATH = CONFIG_DIR / "objects.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_app_settings() -> dict:
    return load_json(APP_SETTINGS_PATH)


def load_capture_region() -> dict:
    return load_json(CAPTURE_REGION_PATH)


def save_capture_region(region: dict) -> None:
    save_json(CAPTURE_REGION_PATH, region)


def load_object_registry() -> dict:
    return load_json(OBJECTS_PATH)


def load_all_config() -> dict:
    return {
        "app_settings": load_app_settings(),
        "capture_region": load_capture_region(),
        "objects": load_object_registry(),
    }