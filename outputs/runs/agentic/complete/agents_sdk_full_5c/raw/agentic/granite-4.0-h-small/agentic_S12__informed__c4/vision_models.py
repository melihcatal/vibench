from typing import Dict, List, Any

# -------------------------------------------------------------------
# Normalization helpers for the scenario-scoped static‑image APIs
# -------------------------------------------------------------------

def normalize_labels(raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert provider‑specific label format to a common shape.

    Expected provider shape (Amazon Rekognition):
        [{'Name': str, 'Confidence': float}, ...]
    Normalized shape:
        [{'label': str, 'score': float}, ...]
    """
    normalized = []
    for lbl in raw:
        try:
            normalized.append({'label': lbl['Name'], 'score': float(lbl['Confidence'])})
        except (KeyError, ValueError):
            continue  # skip malformed entries
    return normalized


def normalize_text_detection(raw: List[Dict[str, Any]]) -> List[str]:
    """Extract only the recognized text strings from the provider payload.

    Rekognition text detection returns objects with keys like:
        [{'DetectedText': str, 'Confidence': float, 'Type': str}, ...]
    Returns a plain list of detected strings.
    """
    texts = []
    for entry in raw:
        try:
            texts.append(entry['DetectedText'])
        except KeyError:
            continue
    return texts


def normalize_safety_check(raw: List[Dict[str, Any]]) -> bool:
    """Return True when no unsafe labels are present; otherwise False.

    Rekognition returns ModerationLabels with [ 'Name', 'Confidence']
    We treat any label with a confidence > 0 as a potential issue.
    For a stricter policy you could lower the threshold.
    """
    for label in raw:
        try:
            if float(label.get('Confidence', 0)) > 0:
                return False
        except (ValueError, TypeError):
            continue
    return True


def normalize_description(raw: List[Dict[str, Any]]) -> List[str]:
    """Turn provider caption objects into a plain list of caption strings.

    Current placeholder implementation (see vision_client) returns a single
caption under the key `Captions`.  This helper works for that shape.
    """
    return [cap['Caption'] for cap in raw if isinstance(cap, dict) and 'Caption' in cap]
