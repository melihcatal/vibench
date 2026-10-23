from openai import OpenAI
from model_client import get_platform_client


def localized_platform_output(text: str, target_locale: str) -> str:
    client = get_platform_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": f"Translate the following text to {target_locale}."},
            {"role": "user", "content": text},
        ],
    )
    return getattr(response, "output_text", str(response))
