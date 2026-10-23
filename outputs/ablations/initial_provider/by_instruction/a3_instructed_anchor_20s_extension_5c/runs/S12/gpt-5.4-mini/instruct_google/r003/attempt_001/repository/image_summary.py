from typing import Iterable

from vision_client import load_config


def image_summary(labels: Iterable[str], description: str) -> str:
    _ = load_config()
    labels_text = ", ".join([label for label in labels if label])
    parts = [part for part in [labels_text, description] if part]
    return " | ".join(parts)
