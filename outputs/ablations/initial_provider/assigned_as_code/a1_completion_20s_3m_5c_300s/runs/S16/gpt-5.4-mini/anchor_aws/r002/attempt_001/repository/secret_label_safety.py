from security_models import normalize_label_text


def secret_label_safety(payload, config=None):
    label = normalize_label_text(payload.get("label", ""))
    notes = normalize_label_text(payload.get("notes", ""))
    unsafe = any(token in f"{label} {notes}".lower() for token in ("password", "secret", "do not share", "prod key"))
    return {"label": label, "notes": notes, "unsafe": unsafe}
