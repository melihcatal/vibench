from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def localized_platform_output(text: str, locale: str = "es") -> str:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    result = client.responses.create(
        model=cfg.model,
        input=f"Translate to {locale}: {normalize_text(text)}",
    )
    return normalize_text(result.output_text)
