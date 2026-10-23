import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class LocalizationConfig:
    api_key: str
    base_url: str
    model: str
    target_locale: str


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_config() -> LocalizationConfig:
    api_key = _env("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return LocalizationConfig(
        api_key=api_key,
        base_url=_env("OPENAI_BASE_URL", "https://api.openai.com/v1") or "https://api.openai.com/v1",
        model=_env("OPENAI_MODEL", "openai/gpt-5.4-mini") or "openai/gpt-5.4-mini",
        target_locale=_env("TARGET_LOCALE", "es-ES") or "es-ES",
    )


def localize_platform_output(platform_output: str) -> str:
    config = load_config()
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {
                "role": "system",
                "content": f"Translate the platform output into {config.target_locale}. Preserve meaning, product names, and formatting.",
            },
            {"role": "user", "content": platform_output},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
