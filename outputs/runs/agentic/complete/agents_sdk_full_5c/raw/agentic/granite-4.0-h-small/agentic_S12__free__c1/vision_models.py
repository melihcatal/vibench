from typing import List, Dict, Any

def normalize_labels(raw: List[Dict[str, Any]]) -> List[str]:
    """Convert raw Google Vision label response to a simple list of label names."""
    return [label['name'] for label in raw]

def normalize_description(raw: str) -> str:
    """Trim whitespace from description and ensure non-empty string."""
    return raw.strip() if raw else ''

def normalize_ocr(raw: List[Dict[str, Any]]) -> List[str]:
    """Extract text from Google Vision text detection response."""
    return [annotation['description'] for annotation in raw]

def normalize_safe_search(raw: Dict[str, Any]) -> str:
    """Map safe search likelihood to a simple rating string."""
    likelihood = raw['adult']
    mapping = {
        'VERY_UNLIKELY': 'Very Low',
        'UNLIKELY': 'Low',
        'POSSIBLE': 'Medium',
        'LIKELY': 'High',
        'VERY_LIKELY': 'Very High'
    }
    return mapping.get(likelihood, 'Unknown')
