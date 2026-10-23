def normalize_description(description):
    return {"description": description}


def normalize_text(text):
    return {"text": text}


def normalize_safety_score(moderation_labels):
    return {"safety_score": sum(label["Confidence"] for label in moderation_labels) / len(moderation_labels) if moderation_labels else 0.0}