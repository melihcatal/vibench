import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_OBJECT_STORAGE_HOST = "https://api.openai.com"
OPENAI_STORAGE_OBJECTS_ENDPOINT = "https://api.openai.com/v1/files"


@dataclass(frozen=True)
class ImageAssetArchiveConfig:
    api_key: str
    endpoint: str = OPENAI_STORAGE_OBJECTS_ENDPOINT
    timeout: float = 60.0


def load_archive_config() -> ImageAssetArchiveConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    endpoint = os.environ.get("OPENAI_FILES_ENDPOINT", OPENAI_STORAGE_OBJECTS_ENDPOINT)
    timeout = float(os.environ.get("OPENAI_ARCHIVE_TIMEOUT", "60"))
    return ImageAssetArchiveConfig(api_key=api_key, endpoint=endpoint, timeout=timeout)


def archive_image_asset(
    asset: Dict[str, Any],
    *,
    caption: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None,
    config: Optional[ImageAssetArchiveConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_archive_config()
    payload = {
        "purpose": "assistants",
        "metadata": {
            "asset": json.dumps(asset, ensure_ascii=False),
            "caption": caption or "",
            "analysis": json.dumps(analysis or {}, ensure_ascii=False),
        },
    }
    response = requests.post(
        cfg.endpoint,
        headers={"Authorization": f"Bearer {cfg.api_key}"},
        data=payload,
        timeout=cfg.timeout,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: image_asset_archive.py '<json-asset>' [caption] [analysis-json]")
    asset = json.loads(sys.argv[1])
    caption = sys.argv[2] if len(sys.argv) > 2 else None
    analysis = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(archive_image_asset(asset, caption=caption, analysis=analysis), ensure_ascii=False))


if __name__ == "__main__":
    main()
