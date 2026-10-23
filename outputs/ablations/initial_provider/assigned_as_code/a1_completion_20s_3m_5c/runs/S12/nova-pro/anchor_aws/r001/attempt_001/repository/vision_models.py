def normalize_image_description(description):
    return description.lower()


def normalize_image_text(text):
    return text.strip()


def normalize_image_safety(safety_score):
    return safety_score