import os

from openai import AzureOpenAI


def localized_platform_output(text: str, target_locale: str) -> str:
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    )
    result = client.responses.create(
        model=os.getenv("AZURE_OPENAI_TRANSLATION_DEPLOYMENT", "gpt-4o-mini"),
        input=f"Translate to {target_locale}: {text}",
    )
    return getattr(result, "output_text", str(result))
