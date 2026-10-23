# vision_models.py
# Normalization and helper utilities for the Static Image & Visual Understanding scenario

from typing import List, Dict

# ----------------------------------------------------------------------------------------------
# Normalizer: unify label outputs from various providers
# ----------------------------------------------------------------------------------------------
def normalize_labels(raw_labels: List[str]) -> List[str]:
    """Clean and deduplicate label strings."""
    return sorted(set(label.strip().lower() for label in raw_labels if label.strip()))

# ----------------------------------------------------------------------------------------------
# Normalizer: standardize short captions
# ----------------------------------------------------------------------------------------------
def normalize_caption(caption: str) -> str:
    """Trim, capitalize, and ensure sentence ending."""
    cap = caption.strip()
    if not cap:
        return "No description available."
    if not cap[-1] in '.!?':
        cap += '.'
    return cap.capitalize()

# ----------------------------------------------------------------------------------------------
# Normalizer: filter out empty OCR results
# ----------------------------------------------------------------------------------------------
def normalize_ocr(texts: List[str]) -> List[str]:
    return [t.strip() for t in texts if t.strip()]

# ----------------------------------------------------------------------------------------------
# Normalizer: collapse safety flags into a concise report
# ----------------------------------------------------------------------------------------------
def normalize_safety(flags: List[str]) -> str:
    if not flags:
        return 'PASS'
    return f'FAIL ({‘, ‘.join(sorted(set(flag.lower() for flag in flags)))})'

# ----------------------------------------------------------------------------------------------
# Example usage (uncomment to test)
# if __name__ == '__main__':
#     print(normalize_labels(['cat', 'Dog', '  cat  ']))
#     print(normalize_caption('a beautiful sunrise over the lake'))
# ----------------------------------------------------------------------------------------------
