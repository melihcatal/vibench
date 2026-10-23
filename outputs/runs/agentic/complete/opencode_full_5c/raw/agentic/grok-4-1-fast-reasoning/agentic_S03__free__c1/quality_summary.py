import openai
import os


def quality_summary(
    original: str, translated: str, source_lang: str, target_lang: str
) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize any quality issues in this translation from {source_lang} to {target_lang}:\\n\\nOriginal: {original}\\nTranslated: {translated}\\n\\nProvide a concise summary."
    completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
