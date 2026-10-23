from vision_client import VisionClient


def check_visual_labels_safety(text: str) -> dict:
    comprehend_client = VisionClient().get_comprehend_client()
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response
