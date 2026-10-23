from __future__ import annotations

from openai import OpenAI

from safety_client import get_openai_api_key, translation_model


def appeal_translate(appeal_text: str, target_language: str = "en", api_key: str | None = None, model: str | None = None) -> str:
    client = OpenAI(api_key=get_openai_api_key(api_key))
    resolved_model = translation_model(model)
    response = client.responses.create(
        model=resolved_model,
        input=(
            f"Translate the following user moderation appeal into {target_language}. "
            "Preserve tone, intent, and references relevant for human review.\n\n"
            f"Appeal: {appeal_text}"
        ),
    )
    return response.output_text
