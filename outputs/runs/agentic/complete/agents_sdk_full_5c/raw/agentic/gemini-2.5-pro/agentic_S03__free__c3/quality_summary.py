import os
from openai import OpenAI

def summarize_translation_quality(original_text: str, translated_text: str, target_language: str) -> str:
    """
    Uses an OpenAI model to summarize potential quality issues in a translation.

    Args:
        original_text: The source text.
        translated_text: The translated text.
        target_language: The name of the target language (e.g., "Spanish").

    Returns:
        A summary of potential quality issues.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Please review the following translation from English to {target_language}.
    Identify any potential issues related to grammar, tone, style, or mistranslation.
    Provide a brief summary of the translation's quality.

    Original Text:
    "{original_text}"

    Translated Text:
    "{translated_text}"

    Quality Summary:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional translation quality reviewer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=250,
    )

    return response.choices[0].message.content or "Could not generate summary."
