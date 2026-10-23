from __future__ import annotations

from model_client import get_azure_openai_client, get_chat_deployment
from model_models import TranslationResult, extract_text_from_response



def localized_platform_output(text: str, target_locale: str) -> TranslationResult:
    client = get_azure_openai_client()
    deployment = get_chat_deployment()
    response = client.responses.create(
        model=deployment,
        input=[
            {
                "role": "system",
                "content": f"Translate the user content into locale {target_locale} while preserving meaning and tone.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        max_output_tokens=600,
    )
    return TranslationResult(
        text=extract_text_from_response(response),
        target_locale=target_locale,
        model=getattr(response, "model", deployment),
        raw=response,
    )
