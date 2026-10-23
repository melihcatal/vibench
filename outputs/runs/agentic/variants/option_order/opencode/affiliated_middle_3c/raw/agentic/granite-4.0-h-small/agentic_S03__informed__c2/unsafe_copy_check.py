# unsafe_copy_check.py – Check localized copy for unsafe content
import json
from typing import List, Dict, Optional

from translation_client import GeneralTextTranslationClient
from translation_models import _normalize_response

# Assume an external content safety SDK or REST client is available.
# For demo purposes we use a placeholder that always returns "safe".
# from content_safety import check_unsafe

SAFETY_CATEGORIES = {
    "unsafe": "Content contains unsafe material",
    "safe": "Content is safe",
}


def check_unsafe_copies(
    copies: List[str], policy: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Flag each translated copy as safe/unsafe according to a content safety service.",
    Args:
        copies (List[str]): List of translated text segments.
        policy (Optional[str]): Policy identifier (e.g., "profanity", "personal_data").
    Returns:
        List[Dict[str, Any]]: Each entry contains the original copy and its safety status.
    """
    results: List[Dict[str, Any]] = []
    for copy in copies:
        # ---- Placeholder safety check ----
        # status = "safe"  # or "unsafe" based on real service call
        status = "safe"
        # ---- End placeholder ----
        results.append({"copy": copy, "safety": SAFETY_CATEGORIES[status]})
    return results


# Example usage (requires a real safety SDK)
# client = GeneralTextTranslationClient()
# raw = client.translate(texts=["Buy 1, get 1 free!"], source_lang="en", target_lang="zh")
# norm = [_normalize_response(r) for r in raw]
# safe_checks = check_unsafe_copies([r["translated_text"] for r in norm])
# print(safe_checks)
