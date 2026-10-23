def normalize_response(response):
    return {
        "labels": [
            {"name": label.description, "confidence": label.score}
            for label in response.label_annotations
        ],
        "text": [text.description for text in response.text_annotations],
        "description": response.text_annotations[0].description if response.text_annotations else "No text found",
        "safety": {
            "adult": response.safe_search_annotation.adult,
            "spoof": response.safe_search_annotation.spoof,
            "medical": response.safe_search_annotation.medical,
            "violence": response.safe_search_annotation.violence,
            "racy": response.safe_search_annotation.racy,
        },
    }