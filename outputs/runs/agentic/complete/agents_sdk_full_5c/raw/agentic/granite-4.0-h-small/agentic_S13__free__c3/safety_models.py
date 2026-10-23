from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class ModerationRequest:
    text: str
    model: str = 'text-moderation-latest'   # concrete OpenAI model identifier

def normalize_scores(raw: Dict[str, float]) -> Dict[str, float]:
    """
    Ensure scores are in 0.0-1.0 range and sort for deterministic ordering.
    """
    return {k: max(0.0, min(1.0, v)) for k, v in raw.items()}

# Example response container
@dataclass(frozen=True)
class ModerationResponse:
    scores: Dict[str, float] = None


def parse_moderation_response(resp: Any) -> ModerationResponse:
    """Extract scores from the provider's raw JSON and normalize."""
    if isinstance(resp, dict) and 'results' in resp:
        result = resp['results'][0]
        scores = result.get('categories', {})
    else:
        scores = {}
    return ModerationResponse(normalize_scores(scores))
