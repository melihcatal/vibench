from openai import AzureOpenAI

from model_client import get_azure_openai_client


def localized_platform_output(text: str, target_locale: str = "es") -> str:
    client: AzureOpenAI = get_azure_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_locale}."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content
