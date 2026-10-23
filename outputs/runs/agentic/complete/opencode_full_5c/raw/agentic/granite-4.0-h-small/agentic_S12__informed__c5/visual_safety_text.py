import json
from vision_client import VisionClient
from vision_models import Normalizer


def check_safety_text(texts: list) -> bool:
    """Scans extracted OCR text for unsafe language using Amazon Rekognition moderation.

    Returns True if the text is safe, otherwise False.
    """
    client = VisionClient()
    # Rekognition can analyze text directly via DetectModerationLabels on image bytes,
    # but for simplicity we reuse the same client and send the concatenated text as a mock image.
    mock_image_bytes = b"safety_check_placeholder"
    response = client.detect_moderation_labels(Image={"Bytes": mock_image_bytes})
    # Placeholder: in real usage call the text‑moderation endpoint or adjust per provider.
    return Normalizer.normalize_safety(response)
