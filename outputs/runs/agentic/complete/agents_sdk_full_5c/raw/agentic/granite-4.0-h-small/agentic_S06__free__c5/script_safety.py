# script_safety.py
# [LATER-STEP] Check narration scripts for unsafe content using Google Cloud Content Safety API.

from google.cloud import content_safety
from speech_client import get_texttospeech_client  # reuse ADC handling

def is_script_safe(script: str, categories: list = ['SEXUAL_CONTENT', 'VIOLENCE', 'HATE_SPEECH']) -> bool:
    """Check if a narration script is safe for synthesis.

    Args:
        script: Plain text or SSML to evaluate.
        categories: List of unsafe categories to filter (defaults to common ones).

    Returns:
        True if safe, False otherwise.
    """
    client = content_safety.Client()  # Uses ADC credentials
    response = client.analyze_content(text=script, categories=categories)
    # response.categories contains detected unsafe categories
    unsafe = response.categories
    return not unsafe
