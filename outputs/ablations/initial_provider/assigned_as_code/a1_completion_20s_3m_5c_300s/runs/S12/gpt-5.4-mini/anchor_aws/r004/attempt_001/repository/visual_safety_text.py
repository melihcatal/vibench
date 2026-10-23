def visual_safety_text(payload, config=None):
    labels = payload.get("labels") or []
    text = payload.get("text") or []
    flagged = []
    for item in labels:
        name = (item.get("name") or "").lower()
        if any(term in name for term in ("weapon", "gun", "knife", "blood", "nude")):
            flagged.append(item.get("name"))
    for item in text:
        value = (item.get("text") or "").lower()
        if any(term in value for term in ("password", "ssn", "credit card", "confidential")):
            flagged.append(item.get("text"))
    return {"unsafe": bool(flagged), "flagged": flagged}
