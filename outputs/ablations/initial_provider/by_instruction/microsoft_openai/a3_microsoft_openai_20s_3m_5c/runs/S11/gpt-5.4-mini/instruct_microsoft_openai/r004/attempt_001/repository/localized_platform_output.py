from openai import AzureOpenAI

from model_client import build_azure_openai_client


def localized_platform_output(text: str, target_locale: str = "es") -> str:
    client = build_azure_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_locale} while preserving meaning."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content
