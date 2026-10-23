import os
from openai import OpenAI

def check_text_for_safety(text_to_check: str) -> bool:
    """
    Uses OpenAI's moderation endpoint to check if secret labels or notes
    contain unsafe or inappropriate text.

    Args:
        text_to_check: The string to analyze.

    Returns:
        True if the text is flagged as unsafe, False otherwise.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable is not set.")
        return True # Default to unsafe if we can't check

    try:
        client = OpenAI(api_key=api_key)
        response = client.moderations.create(
            model="text-moderation-stable",
            input=text_to_check
        )
        
        result = response.results[0]
        return result.flagged

    except Exception as e:
        print(f"An error occurred during OpenAI moderation check: {e}")
        # Fail safe: if the check fails, assume the content might be unsafe.
        return True
