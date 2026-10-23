import os

from openai import AzureOpenAI


def localized_platform_output(text: str, target_locale: str | None = None) -> dict:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )
    locale = target_locale or os.getenv("TARGET_LOCALE", "es")
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": f"Translate into {locale}: {text}"}],
        temperature=0.2,
    )
    return {
        "provider": "azure-openai",
        "locale": locale,
        "raw": response,
        "text": response.choices[0].message.content,
    }
