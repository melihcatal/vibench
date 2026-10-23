from openai import AzureOpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def localized_platform_output(text: str, target_locale: str) -> str:
    config = load_platform_config()
    client: AzureOpenAI = build_platform_client(config)
    response = client.chat.completions.create(
        model=config.deployment,
        messages=[
            {"role": "system", "content": f"Translate into {target_locale}."},
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    choice = response.choices[0]
    return normalize_text(choice.message.content)
