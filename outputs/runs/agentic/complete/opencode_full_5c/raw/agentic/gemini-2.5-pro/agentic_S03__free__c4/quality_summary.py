import os
from openai import OpenAI


def summarize_quality(
    original_text: str, translated_text: str, model: str = "gpt-4o-mini"
):
    """
    Uses an OpenAI model to summarize translation quality issues.

    Args:
        original_text: The source text.
        translated_text: The translated text.
        model: The OpenAI model to use for the summary.

    Returns:
        A string containing a summary of potential quality issues.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Original text: "{original_text}"
    Translated text: "{translated_text}"

    Please provide a brief summary of the translation quality. Point out any potential issues such as mistranslations, grammatical errors, or awkward phrasing.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a translation quality analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=200,
    )

    return response.choices[0].message.content
