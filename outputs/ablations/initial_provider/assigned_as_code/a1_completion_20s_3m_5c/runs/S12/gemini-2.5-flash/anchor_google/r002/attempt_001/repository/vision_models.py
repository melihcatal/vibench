import base64

def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def decode_base64_to_image(base64_string):
    return base64.b64decode(base64_string)

def normalize_labels_response(response):
    return {"labels": [
        {"name": label.description, "confidence": label.score}
        for label in response.label_annotations
    ]}

def normalize_text_detection_response(response):
    texts = [text.description for text in response.text_annotations]
    return {"detected_text": texts[0] if texts else ""}

def normalize_safe_search_response(response):
    safe_search_annotation = response.safe_search_annotation
    return {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
