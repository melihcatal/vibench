from openai import AzureOpenAI

from model_client import get_api_key, get_endpoint


def localized_platform_output(text: str, target_locale: str) -> str:
    client = AzureOpenAI(
        azure_endpoint=get_endpoint(), api_key=get_api_key(), api_version="2024-06-01"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_locale}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
