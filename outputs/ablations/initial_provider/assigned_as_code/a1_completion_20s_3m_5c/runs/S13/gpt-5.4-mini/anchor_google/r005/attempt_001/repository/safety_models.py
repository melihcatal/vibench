import math


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_messages(messages):
    if messages is None:
        return []
    return [normalize_text(message) for message in messages]


def clamp_score(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0
    if math.isnan(value) or math.isinf(value):
        value = 0.0
    return max(0.0, min(1.0, value))


def build_decision(score, threshold):
    score = clamp_score(score)
    threshold = clamp_score(threshold)
    return {"score": score, "threshold": threshold, "allow": score < threshold}
