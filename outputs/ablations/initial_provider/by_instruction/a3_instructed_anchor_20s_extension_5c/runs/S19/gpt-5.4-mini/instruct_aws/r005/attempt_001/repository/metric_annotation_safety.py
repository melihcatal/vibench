import re

from observability_client import load_observability_config


_UNSAFE = re.compile(r"(?:<script|javascript:|data:text/html|onerror\s*=|onload\s*=)", re.IGNORECASE)


def metric_annotation_safety(text: str):
    cfg = load_observability_config()
    unsafe = bool(_UNSAFE.search(text or ""))
    return {"provider": "aws", "region": cfg["aws_region"], "safe": not unsafe}
