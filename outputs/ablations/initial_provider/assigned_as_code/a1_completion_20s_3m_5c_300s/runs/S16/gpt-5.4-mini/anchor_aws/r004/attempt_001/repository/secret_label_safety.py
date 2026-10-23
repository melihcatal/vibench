import re


UNSAFE_PATTERNS = [
    re.compile(r"(?i)password\s*[:=]"),
    re.compile(r"(?i)secret\s*[:=]"),
    re.compile(r"(?i)token\s*[:=]"),
    re.compile(r"(?i)api[_-]?key\s*[:=]"),
]


def secret_label_safety(payload, config=None):
    text = " ".join(str(payload.get(field, "")) for field in ("label", "notes"))
    unsafe = any(pattern.search(text) for pattern in UNSAFE_PATTERNS)
    return {"safe": not unsafe, "label": payload.get("label"), "notes": payload.get("notes")}
