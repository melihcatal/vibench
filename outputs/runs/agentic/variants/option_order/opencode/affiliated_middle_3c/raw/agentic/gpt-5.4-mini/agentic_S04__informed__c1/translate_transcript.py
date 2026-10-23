from openai import OpenAI
from speech_client import load_config


def translate_transcript(text: str, target_language: str) -> str:
    client = OpenAI(api_key=load_config().api_key or "", base_url="https://api.openai.com/v1")
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate the transcript to {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
