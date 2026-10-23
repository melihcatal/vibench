import os
import json
from typing import Dict, Any


def moderate_free_text(
    claims: Dict[str, Any], policy: Dict[str, Any]
) -> Dict[str, Any]:
    """Implement a simple moderation check on free-text claims (e.g., notes, profile bio).
    The function flags or cleans any claim that violates the supplied policy rules.
    Args:
        claims (Dict[str, Any]): Raw federated user claims.
        policy (Dict[str, Any]): Moderation policy, e.g., regex patterns to reject.
    Returns:
        Dict[str, Any]: Cleaned claims with a top-level 'moderation' flag.
    """
    import re

    flagged = False
    cleaned = claims.copy()
    for key, value in claims.items():
        if isinstance(value, str):
            for regex, reason in policy.get("patterns", {}).items():
                if re.search(regex, value, re.IGNORECASE):
                    flagged = True
                    cleaned[key] = "[REDACTED - policy violation: {}]".format(reason)
                    break  # stop checking other patterns for this field
    cleaned["moderation"] = {
        "flagged": flagged,
        "details": [] if not flagged else "Contains prohibited content",
    }
    return cleaned


# Example policy structure:
# {
#     "patterns": {
#         r"\b[hate|slur]\b": "Prohibited hate or slur language",
#         r"\b\d{16}\b": "Potential credit card number"
#     }
# }

# Example usage (for local testing):
# raw = {"bio": "I love coding and hate Mondays", "email": "test@example.com"}
# policy = {
#     "patterns": {r"\bhate\b": "Hate language"}
# }
# print(moderate_free_text(raw, policy))
