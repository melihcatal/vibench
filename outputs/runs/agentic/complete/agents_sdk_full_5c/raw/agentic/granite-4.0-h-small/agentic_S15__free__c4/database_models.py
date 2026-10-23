# [HELPER] database_models.py
import json
import re

def normalize_document(document):
    """Clean and normalize a document before storage.

    - Strip excess whitespace from string values.
    - Remove control characters.
    - Ensure numeric IDs are stored as strings.
    """
    normalized = {}
    for k, v in document.items():
        if isinstance(v, str):
            # Strip leading/trailing whitespace and collapse internal whitespace
            v = re.sub(r'\\s+', ' ', v.strip())
            # Remove non-printable characters except space
            v = ''.join(ch for ch in v if ch.isprintable() or ch.isspace())
            normalized[k] = v
        elif isinstance(v, (int, float)):
            normalized[k] = str(v)  # store numbers as strings to keep DynamoDB homogenous
        elif isinstance(v, (dict, list)):
            normalized[k] = json.dumps(v)
        else:
            normalized[k] = v
    return normalized


def denormalize_document(document):
    """Convert stored values back to native Python types.

    DynamoDB stores numbers and booleans as numbers; we keep everything as strings on write,
    so here we attempt to cast numeric strings back to int/float and re‑parse JSON strings for
    complex objects.
    """
    denorm = {}
    for k, v in document.items():
        if isinstance(v, str):
            # Try to cast to int
            if re.fullmatch(r'-?\\d+', v):
                denorm[k] = int(v)
            elif re.fullmatch(r'-?\\d+\\.\\d+(\\d+)?', v):
                denorm[k] = float(v)
            # Try JSON parsing for objects/lists
            try:
                denorm[k] = json.loads(v)
            except json.JSONDecodeError:
                denorm[k] = v
        else:
            denorm[k] = v
    return denorm


def sanitize_content(text):
    """Simple safety check for user‑generated content.

    - Strip HTML/JS tags.
    - Reject scripts or unsafe patterns.
    """
    if not isinstance(text, str):
        return text
    # Remove any <script> tags or on* attributes
    text = re.sub(r'<[/]?script[^>]*>|on\w+=\"[^\"]*\"', '', text, flags=re.IGNORECASE)
    return text.strip()