from typing import Dict

from openai import OpenAI

from model_client import get_openai_client, get_model_name


def localized_platform_output(text: str, target_locale: str = "es") -> Dict[str, str]:
    client: OpenAI = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    response = client.responses.create(
        model=model,
        input=f"Translate the following text into {target_locale}: {text}",
    )
    return {
        "provider": "openai",
        "model": model,
        "locale": target_locale,
        "text": getattr(response, "output_text", ""),
    }
