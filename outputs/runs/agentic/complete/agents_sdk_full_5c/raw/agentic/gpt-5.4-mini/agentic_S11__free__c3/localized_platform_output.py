from openai import OpenAI

from model_client import build_client, load_config


def localize_platform_output(text: str, target_locale: str = "es") -> str:
    config = load_config()
    client: OpenAI = build_client(config)
    response = client.responses.create(
        model=config.model,
        input=f"Translate the following text to {target_locale}: {text}",
    )
    return response.output_text.strip()
