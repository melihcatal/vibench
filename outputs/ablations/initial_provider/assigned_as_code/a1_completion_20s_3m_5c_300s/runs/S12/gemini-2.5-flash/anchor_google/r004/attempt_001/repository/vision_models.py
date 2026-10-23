def create_image_request(image_bytes: bytes):
    return {"image_bytes": image_bytes}

def create_label_detection_response(labels: list):
    return {"labels": labels}

def create_description_response(description: str):
    return {"description": description}

def create_text_detection_response(full_text: str, detected_texts: list):
    return {"full_text": full_text, "detected_texts": detected_texts}

def create_safe_search_response(adult: str, spoof: str, medical: str, violence: str, racy: str):
    return {"adult": adult, "spoof": spoof, "medical": medical, "violence": violence, "racy": racy}
