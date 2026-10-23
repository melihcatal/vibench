from typing import Union, List, Dict

DEFAULT_THRESHOLDS: Dict[str, float] = {
    'hate': 0.1,
    'harassment': 0.1,
    'self_harm': 0.1,
    'sexual': 0.1,
    'violence': 0.1,
}

def normalize_input(text: Union[str, List[str]]) -> Union[str, List[str]]:
    if isinstance(text, str):
        return text.strip()
    return [t.strip() for t in text if t.strip()]
