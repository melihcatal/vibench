import os
import cohere

def translate_transcript_segment(text: str, target_language: str = "French") -> str:
    """
    Translates a text segment using Cohere.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into.

    Returns:
        The translated text.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)

    prompt = f"Translate the following English text to {target_language}: '{text}'"
    
    response = co.chat(
        message=prompt,
        model="command-r"
    )
    
    return response.text
