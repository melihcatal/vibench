def normalize_label_response(response):
    return [{"name": label.description, "confidence": label.score} for label in response.label_annotations]


def normalize_text_response(response):
    return [text.description for text in response.text_annotations]


def normalize_safety_response(response):
    return response.safe_search_annotation.to_dict()