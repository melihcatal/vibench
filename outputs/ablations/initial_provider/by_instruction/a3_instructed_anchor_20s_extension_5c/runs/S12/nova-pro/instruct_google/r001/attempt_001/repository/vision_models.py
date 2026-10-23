from google.cloud import vision

def normalize_labels(response):
    return [label.description for label in response.label_annotations]

def normalize_text(response):
    return [text.description for text in response.text_annotations]

def normalize_safety(response):
    return response.safe_search_annotation