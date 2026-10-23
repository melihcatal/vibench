import os
import openai

def summarize_quality(source_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """
    Uses an LLM to provide a quality summary of a translation.

    Args:
        source_text: The original text.
        translated_text: The text after translation.
        source_lang: The source language name (e.g., "English").
        target_lang: The target language name (e.g., "French").

    Returns:
        A string containing a summary of potential quality issues.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    You are a linguistic expert tasked with assessing translation quality.
    Please analyze the following translation from {source_lang} to {target_lang}.
    Provide a brief, neutral summary of potential quality issues.
    Consider aspects like grammatical errors, awkward phrasing, loss of nuance, or mistranslations.
    If the translation is excellent, please state that.

    Source ({source_lang}):
    "{source_text}"

    Translation ({target_lang}):
    "{translated_text}"

    Quality Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a linguistic expert providing translation quality analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate a quality summary."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"

