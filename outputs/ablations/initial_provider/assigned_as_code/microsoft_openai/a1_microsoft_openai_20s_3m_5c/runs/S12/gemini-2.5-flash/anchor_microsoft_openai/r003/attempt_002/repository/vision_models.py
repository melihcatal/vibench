"""
Define local request, response, and normalization helpers for Static Image and Visual Understanding.
For simplicity, using dictionaries with expected keys.
"""

def normalize_labels_response(labels_data: list) -> dict:
    # Expected labels_data format: [{'name': 'tag_name', 'confidence': 0.9}]
    return {"labels": labels_data}

def normalize_description_response(description: str) -> dict:
    # Expected description format: "A short description of the image."
    return {"description": description}

def normalize_text_detection_response(full_text: str, words: list) -> dict:
    # Expected full_text format: "Full text detected in image"
    # Expected words format: ["word1", "word2"]
    return {"full_text": full_text, "words": words}

def normalize_safety_score_response(safety_scores: dict) -> dict:
    # Expected safety_scores format: {'adult': 'VERY_UNLIKELY', 'spoof': 'UNLIKELY', ...}
    return {"safety_scores": safety_scores}

def normalize_summary_response(summary: str) -> dict:
    return {"summary": summary}

def normalize_translation_response(translated_text: str) -> dict:
    return {"translated_text": translated_text}

def normalize_text_safety_response(safety_verdict: dict) -> dict:
    return {"safety_verdict": safety_verdict}

def normalize_archive_response(archive_status: str, blob_name: str) -> dict:
    return {"archive_status": archive_status, "blob_name": blob_name}
