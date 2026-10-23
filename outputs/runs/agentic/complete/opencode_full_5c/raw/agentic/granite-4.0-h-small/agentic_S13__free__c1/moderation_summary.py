```python
# moderation_summary.py
# LATER-STEP: Summarize moderation decisions

from safety_models import SafetyResponse
from typing import List, Dict

def summarize_decisions(results: List[Dict]) -> Dict:
    """
    Aggregate per-item moderation results into a concise summary.
    Returns {
        'total': int,
        'unsafe': int,
        'unsafe_details': {
            'categories': List[str],
            'example_texts': List[str]
        }
    }
    """
    unsafe_categories = set()
    unsafe_texts = []
    for res in results:
        if not res.get('allow', True):
            unsafe_texts.append(res.get('original_text', 'N/A'))
            for cat in res.get('reasons', []):
                unsafe_categories.add(cat)
    return {
        'total': len(results),
        'unsafe': len(unsafe_texts),
        'unsafe_details': {
            'categories': list(unsafe_categories),
            'example_texts': unsafe_texts[:5]  # show up to 5 examples
        }
    }
```