import os
from openai import OpenAI


def load_platform_config():
    return {
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
        "AZURE_OPENAI_MODEL": os.getenv("AZURE_OPENAI_MODEL", "gpt-4.1-mini"),
    }


def build_openai_client() -> OpenAI:
    cfg = load_platform_config()
    return OpenAI(
        api_key=cfg["AZURE_OPENAI_API_KEY"],
        base_url=f"{cfg['AZURE_OPENAI_ENDPOINT'].rstrip('/')}/openai/v1"
        if cfg["AZURE_OPENAI_ENDPOINT"]
        else None,
    )


def load_prompt(value: str) -> str:
    return value.strip()
