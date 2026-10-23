import re

from observability_client import load_observability_config


_UNSAFE = re.compile(r"(<script|javascript:|data:text/html|onerror=|onload=)", re.IGNORECASE)


def metric_annotation_safety(text: str):
    load_observability_config()
    unsafe = bool(_UNSAFE.search(text or ""))
    return {"safe": not unsafe, "unsafe_patterns": [m.group(0) for m in _UNSAFE.finditer(text or "")]}
