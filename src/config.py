from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

CONFIG_FILE = ".yvd-config.json"


@dataclass
class AppConfig:
    output_dir: str = "downloads"
    default_audio_format: str = "mp3"
    default_audio_quality: str = "best"
    default_video_format: str = "mp4"
    default_video_quality: str = "best"


def load_config(path: str | Path = CONFIG_FILE) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig()

    try:
        raw_data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AppConfig()

    if not isinstance(raw_data, dict):
        return AppConfig()

    valid_keys = {field.name for field in fields(AppConfig)}
    clean_data: dict[str, str] = {}
    for key, value in raw_data.items():
        if key in valid_keys and isinstance(value, str) and value.strip():
            clean_data[key] = value.strip()

    return AppConfig(**clean_data)


def save_config(config: AppConfig, path: str | Path = CONFIG_FILE) -> None:
    config_path = Path(path)
    config_path.write_text(
        json.dumps(asdict(config), indent=2, sort_keys=True),
        encoding="utf-8",
    )
