from vision_client import call_vision_api, OPENAI_VISION_MODEL
from vision_models import TranslationRequest, TranslationResponse


def translate_alt_text(
    request: TranslationRequest, model: str | None = None
) -> TranslationResponse:
    system_prompt = (
        "You are a professional translator specializing in image alt-text translation. "
        "Translate the provided image description accurately while preserving visual details "
        "and accessibility context."
    )
    source_hint = ""
    if request.source_language != "auto":
        source_hint = f" (source language: {request.source_language})"

    user_prompt = (
        f"Translate the following image alt-text to {request.target_language}{source_hint}:\n\n"
        f'"{request.text}"\n\n'
        "Provide only the translated text without additional commentary."
    )

    raw_output = call_vision_api(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=256,
    )

    translated = raw_output.strip().strip('"').strip("'")

    return TranslationResponse(
        translated_text=translated,
        source_language_detected=request.source_language,
        target_language=request.target_language,
    )


def batch_translate_alt_texts(
    texts: list[str],
    target_language: str,
    source_language: str = "auto",
    model: str | None = None,
) -> list[TranslationResponse]:
    results = []
    for text in texts:
        req = TranslationRequest(
            text=text,
            target_language=target_language,
            source_language=source_language,
        )
        result = translate_alt_text(req, model=model)
        results.append(result)
    return results
