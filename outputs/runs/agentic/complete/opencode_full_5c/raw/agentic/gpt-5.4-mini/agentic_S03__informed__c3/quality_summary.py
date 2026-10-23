import os

from openai import OpenAI


def quality_summary(translated_text, source_language=None, target_language=None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize translation quality issues concisely."},
            {"role": "user", "content": f"Source language: {source_language}
Target language: {target_language}
Text: {translated_text}"},
        ],
    )
    return response.choices[0].message.content
