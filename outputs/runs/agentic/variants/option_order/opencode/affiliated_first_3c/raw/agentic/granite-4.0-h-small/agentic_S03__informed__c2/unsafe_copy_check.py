import html
import re
from translation_client import TranslationClient


def check_unsafe(localized_copy: str) -> bool:
    """Check localized copy for unsafe or malicious content.
    Uses a simple heuristic placeholder for real moderation APIs.
    """
    # Placeholder: replace with real moderation API call
    return any(
        word in localized_copy.lower() for word in ["script", "iframe", "onerror"]
    )


if __name__ == "__main__":
    sample = "Click <a href='javascript:alert(1)'>here</a>"
    print("Unsafe" if check_unsafe(sample) else "Safe")
