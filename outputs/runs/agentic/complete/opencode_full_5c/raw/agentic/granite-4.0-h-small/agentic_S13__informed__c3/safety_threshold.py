# safety_threshold.py
# [SAME-SCENARIO] Applies category thresholds to decide whether to allow text

from safety_client import parse_response
from safety_models import Response

# Provider selection – the concrete service used (kept for visibility)
PROVIDER = (
    "azure"  # Azure AI Content Safety (REST) – can be swapped for another provider
)

# -----------------------------------------------------------------------------
# Configuration: per‑category severity thresholds (e.g., 'moderate' vs 'severe')
# -----------------------------------------------------------------------------
THRESHOLDS = {
    # Category name -> minimum severity that is considered a violation
    # Severity levels (example ordering): none < slight < moderate < severe
    "harassment": "moderate",
    "self_harm": "severe",
    "hate": "moderate",
    "violence": "severe",
    # Extend with additional categories as needed
}

# Helper to map severity strings to numeric ranks for comparison
SEVERITY_RANK = {"none": 0, "slight": 1, "moderate": 2, "severe": 3}


# -----------------------------------------------------------------------------
# Public API: decide whether a single moderated text passes policy thresholds
# -----------------------------------------------------------------------------
def allow_text(moderation: Response) -> bool:
    """Return True if the moderated text complies with the configured thresholds.

    Args:
        moderation: Normalized moderation response from parse_response().

    Returns:
        bool: True if all detected categories meet or are below the defined thresholds,
              False if any category exceeds its allowed severity.
    """
    # If the overall content is marked unsafe, we treat it as a violation
    if not moderation.get("unsafe", False):
        return True

    # Check each detected category against its threshold
    for category, details in moderation.get("categories", {}).items():
        severity = details.get("severity", "none").lower()
        threshold = THRESHOLDS.get(category, "none").lower()
        # If provider severity is higher (numerically) than the allowed threshold, flag violation
        if SEVERITY_RANK.get(severity, 0) > SEVERITY_RANK.get(threshold, 0):
            return False
    return True


# -----------------------------------------------------------------------------
# Public API: apply thresholds to a batch of moderated texts
# -----------------------------------------------------------------------------
def allow_batch(moderations: list) -> list:
    """Apply thresholds to a list of moderated responses.

    Args:
        moderations: List of Response objects from moderate_batch().

    Returns:
        List of booleans corresponding to each moderation.
    """
    return [allow_text(m) for m in moderations]


# Example usage (would live in a driver script):
# decisions = allow_batch(moderate_batch(["I really like you", "You are a jerk!"]))
# print(decisions)  # [True, False]
