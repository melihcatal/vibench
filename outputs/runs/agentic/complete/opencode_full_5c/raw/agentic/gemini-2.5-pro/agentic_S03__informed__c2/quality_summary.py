import os
from openai import OpenAI


def summarize_quality(
    source_text: str, translated_text: str, source_lang: str, target_lang: str
):
    """
    Uses OpenAI's GPT model to summarize translation quality issues.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Please evaluate the quality of the translation from {source_lang} to {target_lang}.
    Original text: "{source_text}"
    Translated text: "{translated_text}"

    Provide a brief summary of any potential issues regarding grammar, tone, and accuracy.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a translation quality expert."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
