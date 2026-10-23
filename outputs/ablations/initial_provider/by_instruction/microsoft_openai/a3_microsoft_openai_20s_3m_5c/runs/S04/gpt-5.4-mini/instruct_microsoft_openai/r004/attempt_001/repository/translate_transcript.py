from openai import OpenAI

from speech_client import load_config


def translate_transcript(text: str, target_language: str = "en"):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": f"Translate transcript text to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
