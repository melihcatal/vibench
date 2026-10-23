import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_default_platform_model_name


def localized_platform_output(text: str, target_locale: str) -> str:
    client: AzureOpenAI = build_azure_openai_client()
    prompt = f"Translate the following into {target_locale} while preserving meaning:\n{text}"
    response = client.responses.create(model=get_default_platform_model_name(), input=prompt)
    return getattr(response, "output_text", "")


if __name__ == "__main__":
    print(localized_platform_output(os.environ.get("PLATFORM_TEXT", ""), os.environ.get("TARGET_LOCALE", "es")))
