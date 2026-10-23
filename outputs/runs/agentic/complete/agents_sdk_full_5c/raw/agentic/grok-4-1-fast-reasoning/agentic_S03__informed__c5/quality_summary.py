import os
from openai import OpenAI

def quality_summary(original: str, translated: str, target_lang: str) -> str:
    """
    Summarize translation quality issues using GPT model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
    Analyze the following translation from English to {target_lang} and summarize any quality issues such as accuracy, fluency, naturalness, or cultural appropriateness.

    Original: {original}

    Translated: {translated}

    Provide a concise summary of issues, or "High quality, no major issues" if good.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
