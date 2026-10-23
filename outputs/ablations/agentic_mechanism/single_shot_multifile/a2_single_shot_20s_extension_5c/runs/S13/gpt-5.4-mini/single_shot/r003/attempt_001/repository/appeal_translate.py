from typing import Dict

from openai import OpenAI

from safety_client import load_safety_config


def appeal_translate(text: str, target_language: str) -> Dict[str, str]:
    config = load_safety_config()
    client = OpenAI(api_key=config.openai_api_key)
    prompt = f"Translate this moderation appeal into {target_language} while preserving tone and meaning: {text}"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return {"translated_text": response.output_text, "model": "gpt-4.1-mini", "target_language": target_language}
