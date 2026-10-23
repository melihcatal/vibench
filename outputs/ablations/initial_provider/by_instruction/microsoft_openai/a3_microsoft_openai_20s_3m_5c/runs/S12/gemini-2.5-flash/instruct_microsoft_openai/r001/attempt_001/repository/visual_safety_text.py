from vision_client import VisionClient
from vision_models import normalize_comprehend_safety_response

def check_visual_labels_safety(text_labels: list[str]) -> list[dict]:
    client_helper = VisionClient()
    comprehend_client = client_helper.get_comprehend_client()

    if not text_labels:
        return []

    # Comprehend batch_detect_toxic_content supports up to 100 documents
    # and each document up to 100KB.
    # For simplicity, we'll join all labels into one text for analysis, assuming it won't exceed limits.
    combined_text = ". ".join(text_labels)
    if not combined_text.strip():
        return []

    try:
        # Using 'en' for English, as it's a common default for safety checks.
        # If the labels could be in other languages, language detection would be needed first.
        response = comprehend_client.batch_detect_toxic_content(
            TextList=[combined_text],
            LanguageCode='en' # AWS Specific
        )
        return normalize_comprehend_safety_response(response)
    except Exception as e:
        print(f"Error checking visual labels safety: {e}")
        return []
