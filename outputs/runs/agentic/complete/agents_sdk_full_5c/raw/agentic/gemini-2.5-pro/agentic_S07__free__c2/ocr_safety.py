
import cohere
import os
from typing import List

class ModerationResult(object):
    def __init__(self, is_unsafe: bool, classifications: dict):
        self.is_unsafe = is_unsafe
        self.classifications = classifications

def check_text_safety(text: str) -> ModerationResult:
    """
    Checks text for unsafe content using the Cohere Moderation API.

    Requires the COHERE_API_KEY environment variable to be set.

    Args:
        text: The input text to moderate.

    Returns:
        A ModerationResult object indicating if the text is unsafe and
        providing classification details.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)

    response = co.moderate(texts=[text])
    
    result = response.results[0]
    
    # Example logic: consider unsafe if any category has high confidence
    is_unsafe = (
        result.toxic > 0.8 or
        result.insult > 0.8 or
        result.hate > 0.8
    )
    
    classifications = {
        'toxic': result.toxic,
        'insult': result.insult,
        'hate': result.hate,
        'profanity': result.profanity,
        'violence': result.violence,
    }

    return ModerationResult(is_unsafe=is_unsafe, classifications=classifications)
