from openai import OpenAI
from speech_client import load_config


def translate_transcript(text: str, target_language: str = "en"):
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key, organization=cfg.organization, project=cfg.project)
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate transcript text accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
