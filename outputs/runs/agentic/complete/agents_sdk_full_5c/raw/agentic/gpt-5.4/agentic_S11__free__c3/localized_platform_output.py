from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import LocalizedOutput
from select_platform_resource import select_platform_resource


def localized_platform_output(text: str, locale: str = "fr-FR") -> LocalizedOutput:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="translation")
    response = client.chat.completions.create(
        model=resource.deployment_name or resource.model_id,
        messages=[
            {
                "role": "system",
                "content": f"Translate the user's text to locale {locale} while preserving meaning and tone.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.2,
        max_tokens=512,
    )
    return LocalizedOutput(locale=locale, text=response.choices[0].message.content or "", raw=response)
