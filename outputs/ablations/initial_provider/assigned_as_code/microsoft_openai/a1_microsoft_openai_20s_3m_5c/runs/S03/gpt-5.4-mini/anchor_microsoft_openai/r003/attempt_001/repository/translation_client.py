import os
from dataclasses import dataclass


@dataclass
class TranslationConfig:
    api_key: str
    region: str
    endpoint: str = "https://api.cognitive.microsofttranslator.com"


def load_translation_config(config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("AZURE_TRANSLATOR_KEY")
    region = config.get("region") or os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = config.get("endpoint") or os.environ.get("AZURE_TRANSLATOR_ENDPOINT") or "https://api.cognitive.microsofttranslator.com"
    if not api_key or not region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are required")
    return TranslationConfig(api_key=api_key, region=region, endpoint=endpoint)


def build_headers(cfg):
    return {
        "Ocp-Apim-Subscription-Key": cfg.api_key,
        "Ocp-Apim-Subscription-Region": cfg.region,
        "Content-Type": "application/json",
    }


def translation_url(cfg, path):
    return cfg.endpoint.rstrip("/") + path
