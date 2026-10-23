import json
from typing import List, Dict

class ModerationResult:
    """Normalized representation of moderation output from any provider.

    Attributes:
        status (str): overall decision (e.g., 'SAFE', 'UNSAFE').
        labels (List[str]): list of detected unsafe categories.
        confidence (float): confidence score for the overall decision.
    """
    def __init__(self, status: str, labels: List[str], confidence: float):
        self.status = status
        self.labels = labels
        self.confidence = confidence

    def to_dict(self) -> dict:
        return {
            'status': self.status,
            'labels': self.labels,
            'confidence': self.confidence
        }

    @classmethod
    def from_provider_response(cls, provider_response: dict) -> 'ModerationResult':
        """Convert a raw provider response to the normalized ModerationResult.

        This example supports the Comprehend format:
        {
            'Sentiment': 'POSITIVE',                # treated as status
            'SentimentScore': {'POSITIVE': 0.97},   # used for confidence
            'Labels': [{'Name': 'TOXICITY', 'Score': 0.85}, ...]
        }
        """
        # Normalize status
        status_map = {
            'POSITIVE': 'SAFE',
            'NEGATIVE': 'UNSAFE'
        }
        status = status_map.get(provider_response.get('Sentiment'), 'UNKNOWN')

        # Extract labels and confidence
        labels = []
        confidence = 0.0
        labels_raw = provider_response.get('Labels', [])
        for lbl in labels_raw:
            name = lbl.get('Name')
            score = lbl.get('Score', 0.0)
            if score > 0.5:  # treat as flagged
                labels.append(name)
            if score > confidence:
                confidence = score
        return cls(status=status, labels=labels, confidence=confidence)
