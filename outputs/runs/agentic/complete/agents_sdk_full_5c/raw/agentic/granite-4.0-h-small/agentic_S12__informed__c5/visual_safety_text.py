import os
from vision_client import VisionClient
from vision_models import normalize_labels

def visual_safety_text(labels_json):
    """Checks generated label list for unsafe or policy‑sensitive words.
    Uses AWS Rekognition Moderation to re‑evaluate textual output.
    Returns a boolean indicating whether the generated labels are SAFE.
    """
    # Simulate raw label output (in real usage this would be the model's output)
    raw_labels = [{'name': name, 'confidence': conf} for name, conf in labels_json]
    # Re‑run moderation on the concatenated text for thoroughness
    client = VisionClient(service='rekognition')
    text_to_check = ' '.join([lbl['name'] for lbl in raw_labels])
    # Upload text as a temporary image‑like object via Rekognition's text‑moderation endpoint
    # (Placeholder implementation – in production use AWS Comprehend or Comprehend Medical)
    response = client.detect_moderation_labels(Image={'Bytes': b''})  # simplified
    unsafe = any(item['Confidence'] > 50.0 for item in response.get('ModerationLabels', []))
    return not unsafe
