import os

from openai import OpenAI


def unsafe_copy_check(text, locale=None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Check localized copy for unsafe content and return a concise assessment."},
            {"role": "user", "content": f"Locale: {locale}
Text: {text}"},
        ],
    )
    return response.choices[0].message.content
