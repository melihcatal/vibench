import os
import json
from typing import Dict

DEFAULT_THRESHOLDS = {
    "toxic": 0.7,
    "obscene": 0.8,
    "hate": 0.5,
    "identity_hate": 0.6,
}


def get_thresholds() -> Dict[str, float]:
    thresholds_str = os.getenv("SAFETY_THRESHOLDS")
    if thresholds_str:
        return json.loads(thresholds_str)
    return DEFAULT_THRESHOLDS
