# platform_output_safety.py
# [LATER-STEP] Check platform model output for unsafe content

import re
from typing import Any, Dict, List

def contains_unsafe_content(text: str) -> bool:
    """Naive heuristic to detect profanity, hate speech, sexual content, or self-harm.

    Returns True if any unsafe pattern is matched.
    """
    unsafe_patterns = [
        r"\b(?:fuck|shit|bitch|cunt|nigger|slut|whore)\b",
        r"\b(?:kill|suicide|self-harm|cutting|depression|depressed)\b",
        r"\b(?:sex|porn|incest|rape)\b",
        r"\b(?:drugs|cocaine|heroin|meth|weed|alcohol abuse)\b",
        r"\b(?:bomb|gun|weapon|terrorism)\b",
    ]
    for pat in unsafe_patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            return True
    return False


def safe_output_check(provider_response: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap provider response with safety flag and (optional) cleaned text.

    Returns a dict:
        {
            'output': original provider response,
            'unsafe': bool,
            'cleaned_text': None or safe version
        }
    """
    # Consolidate all text chunks (choices delta content) into a single string
    choices = provider_response.get('choices', [])
    raw_text = ' '.join(choice.get('delta', {}).get('content', '') for choice in choices)
    unsafe = contains_unsafe_content(raw_text)
    cleaned_text = None
    if unsafe:
        # Simple redaction: replace unsafe words with asterisks
        for pat in [r"\b(?:fuck|shit|bitch|cunt|nigger|slut|whore)\b",
                    r"\b(?:kill|suicide|self-harm)\b"]:
            raw_text = re.sub(pat, "[REDACTED]", raw_text, flags=re.IGNORECASE)
        cleaned_text = raw_text
    return {
        "output": provider_response,
        "unsafe": unsafe,
        "cleaned_text": cleaned_text,
    }

if __name__ == "__main__":
    # Example usage with a dummy response
    dummy = {
        "choices": [
            {
                "delta": {
                    "content": "You should not talk about sex."
                }
            }
        ]
    }
    print(safe_output_check(dummy))
