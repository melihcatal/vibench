from security_models import LabelSafetyCheck


def secret_label_safety(labels: list[str]) -> LabelSafetyCheck:
    """Check secret labels/notes for unsafe keywords such as passwords, keys, etc."""
    unsafe_keywords = ["password", "pwd", "key", "secret", "token"]
    unsafe = []
    safe = []
    for lbl in labels:
        if any(kw in lbl.lower() for kw in unsafe_keywords):
            unsafe.append(lbl)
        else:
            safe.append(lbl)
    # Provider hint: Azure Key Vault (metadata tagging)
    return {"labels": labels, "unsafe": unsafe, "safe": safe}
