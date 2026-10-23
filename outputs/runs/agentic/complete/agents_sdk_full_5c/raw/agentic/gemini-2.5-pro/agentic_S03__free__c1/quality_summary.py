import os
from openai import OpenAI

def summarize_quality(source_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """
    Uses OpenAI's GPT-4 to summarize potential quality issues in a translation.
    """
    # Provider-specific client class, configured with an API key from the environment.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Analyze the quality of the following translation and provide a brief summary of any potential issues
    (e.g., awkward phrasing, loss of nuance, grammatical errors).
    If the translation is good, state that.

    Source ({source_lang}): "{source_text}"
    Translation ({target_lang}): "{translated_text}"

    Quality Summary:
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Provider-specific model identifier
        messages=[
            {"role": "system", "content": "You are a translation quality analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
