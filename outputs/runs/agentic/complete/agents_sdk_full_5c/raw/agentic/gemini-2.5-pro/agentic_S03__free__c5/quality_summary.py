import os
import cohere

def summarize_quality(source_text: str, translated_text: str) -> str:
    """
    Uses Cohere to summarize potential quality issues in a translation.

    Args:
        source_text: The original text.
        translated_text: The translated text.

    Returns:
        A summary of potential quality issues.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)

    prompt = f"""
    Analyze the translation quality from the source text to the translated text.
    Identify any potential issues such as mistranslations, loss of nuance, grammatical errors, or awkward phrasing.
    Provide a concise summary of the findings.

    Source Text: "{source_text}"
    Translated Text: "{translated_text}"

    Quality Summary:
    """

    response = co.chat(
        model="command-r",
        message=prompt,
        temperature=0.3,
    )
    
    return response.text
