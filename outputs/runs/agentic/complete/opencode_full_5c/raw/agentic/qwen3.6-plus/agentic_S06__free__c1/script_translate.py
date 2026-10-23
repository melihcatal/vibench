from __future__ import annotations

from speech_client import create_openai_client, OPENAI_CHAT_MODEL
from speech_models import TranslationRequest, TranslationResponse, normalize_text


def translate_script(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    preserve_formatting: bool = True,
    model: str | None = None,
    api_key: str | None = None,
) -> TranslationResponse:
    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Input text is empty")

    selected_model = model or OPENAI_CHAT_MODEL

    client = create_openai_client(api_key=api_key)

    formatting_instruction = (
        " Preserve all line breaks, punctuation, and formatting exactly."
        if preserve_formatting
        else ""
    )

    system_prompt = (
        f"You are a professional translator. Translate the following text from "
        f"{source_language} to {target_language}.{formatting_instruction} "
        f"Return only the translated text with no additional commentary."
    )

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": normalized},
        ],
        temperature=0.3,
    )

    translated_text = response.choices[0].message.content.strip()

    return TranslationResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        model=selected_model,
    )
