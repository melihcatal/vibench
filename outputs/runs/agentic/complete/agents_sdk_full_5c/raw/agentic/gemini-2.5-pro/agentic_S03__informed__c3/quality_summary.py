import os
from openai import OpenAI

def summarize_quality(source_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """
    Uses an OpenAI model to summarize the quality of a translation.

    Args:
        source_text: The original text.
        translated_text: The translated text.
        source_lang: The source language name (e.g., "English").
        target_lang: The target language name (e.g., "Spanish").

    Returns:
        A summary of the translation quality.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Please evaluate the quality of the following translation from {source_lang} to {target_lang}.
    Provide a brief, one-paragraph summary of potential issues, such as loss of nuance,
    grammatical errors, or awkward phrasing. If the translation is excellent, state that.

    Source Text ({source_lang}):
    "{source_text}"

    Translated Text ({target_lang}):
    "{translated_text}"

    Quality Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional translation quality analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=200,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"

