from typing import List, Dict

# Request model that mirrors the external provider's expected payload
class ModerationRequest:
    def __init__(self, text: str, model: str = "content-safety-gpt-4") -> None:
        self.text = text
        self.model = model

# Response model that normalizes the external provider's output
class ModerationResponse:
    def __init__(self, results: List[List[Dict]]) -> None:
        """
        results: List of per‑input result groups. Each group contains a list of
        flag objects. This mirrors the structure of OpenAI's moderation response.
        """
        self.results = results

    def as_dict(self) -> Dict[str, float]:
        """Flatten scores into a simple dict for per‑category threshold checks."""
        # Example normalization: assume each result group has categories as keys
        # Here we just return the first group's scores for illustration.
        # In real usage you would map the provider's category names to our keys.
        first_group = self.results[0]
        normalized = {}
        for flag in first_group:
            # Provider may include a 'categories' dict; we emulate it.
            # For this stub we fabricate dummy categories.
            normalized.update(flag.get('categories', {}))
        return normalized
