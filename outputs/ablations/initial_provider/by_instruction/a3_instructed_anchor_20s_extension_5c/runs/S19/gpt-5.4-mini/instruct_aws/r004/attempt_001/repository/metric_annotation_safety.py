from typing import Dict


def metric_annotation_safety(text: str) -> Dict[str, object]:
    unsafe = any(token in text.lower() for token in ["<script", "javascript:", "data:text/html", "onerror=", "onload="])
    return {"safe": not unsafe, "provider": "AWS", "checked_text": text}
