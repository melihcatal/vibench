from openai import OpenAI

from speech_client import openai_client_kwargs


def translate_transcript(text: str, target_language: str):
    client = OpenAI(**openai_client_kwargs())
    prompt = f"Translate the following transcript into {target_language}:\n{text}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
