import os
import anthropic

def summarize_quality(source_text: str, translated_text: str, target_language: str) -> str:
    """
    Uses Anthropic's Claude model to summarize potential quality issues in a translation.

    Args:
        source_text: The original text.
        translated_text: The translated text.
        target_language: The target language of the translation.

    Returns:
        A summary of potential quality issues.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""You are a translation quality expert.
Analyze the following source text and its translation into {target_language}.
Identify any potential issues such as mistranslations, grammatical errors, awkward phrasing, or loss of nuance.
Provide a brief, bulleted summary of the issues. If there are no obvious issues, state that the translation appears to be of good quality.

Source Text:
"{source_text}"

Translated Text:
"{translated_text}"

Quality Summary:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text
