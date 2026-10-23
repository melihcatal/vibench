import os
from typing import Dict

DEFAULT_THRESHOLDS: Dict[str, float] = {
    'TOXICITY': 0.7,
    'SEVERE_TOXICITY': 0.9,
    'IDENTITY_ATTACK': 0.8,
    'INSULT': 0.7,
    'PROFANITY': 0.8,
    'THREAT': 0.9,
    'SEXUALLY_EXPLICIT': 0.9,
    'HATE': 0.8,
    'toxicity': 0.5,
    'hate': 0.8,
    'sexual': 0.8,
    'violence': 0.8,
    'self_harm': 0.9
}