from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ModerationResult:
    unsafe: bool
    categories: Dict[str, float]
    spans: List[str] = None


class SafetyResponse:
    def __init__(self, raw_response: Dict):
        self.raw = raw_response

    @property
    def unsafe(self) -> bool:
        return self.raw.get("unsafe", False)

    @property
    def categories(self) -> Dict[str, float]:
        # Returns a dict of category scores; default to 0.0 when missing
        return {k: v for k, v in self.raw.get("categories", {}).items()}

    @property
    def unsafe_spans(self) -> List[str]:
        return self.raw.get("unsafe_spans", [])


def parse_response(raw: Dict) -> SafetyResponse:
    """Normalize a provider's raw response into a consistent SafetyResponse."""
    # Here we assume the provider returns a dict similar to PerspectiveAPI's format
    # with fields: unsafe (bool), categories (dict), unsafe_spans (list).
    # Implement adapters for each provider inside this function if needed.
    return SafetyResponse(raw)


def normalize_score(response: SafetyResponse) -> Dict[str, float]:
    """Convert raw scores to a standard 0.0‑1.0 confidence dict."""
    # Simple passthrough; providers that return raw scores can be normalized here.
    return response.categories


def get_unsafe_message(response: SafetyResponse) -> str:
    """Return a short human readable message summarizing the moderation decision."""
    if response.unsafe:
        return "❗ Unsafe content detected."
    return "✅ Content is acceptable."


def get_category_summary(response: SafetyResponse) -> str:
    """Create a concise summary of category scores."""
    if not response.categories:
        return "No category scores available."
    lines = [f"  {cat}: {score:.2f}" for cat, score in response.categories.items()]
    return "\n".join(["Category scores:", *lines])


def get_unsafe_spans_summary(response: SafetyResponse) -> str:
    """List detected unsafe spans if any."""
    spans = response.unsafe_spans
    if not spans:
        return "No unsafe spans found."
    return "\n".join(["Detected unsafe spans:", *["- " + s for s in spans]])
