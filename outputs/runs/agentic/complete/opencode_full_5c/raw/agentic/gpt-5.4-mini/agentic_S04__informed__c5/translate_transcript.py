from openai import OpenAI

from speech_models import TranslationRequest


def translate_transcript(text, target_language):
    client = OpenAI()
    prompt = f"Translate the following transcript to {target_language} and return only the translation:\n{text}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return {
        "target_language": target_language,
        "translation": resp.choices[0].message.content,
    }
