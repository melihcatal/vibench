"""
Translates generated model output using OpenAI GPT-4o hosted LLM.

Provider: OpenAI (api.openai.com)
Model family: gpt-4o
"""

from typing import Optional

from model_client import (
    get_sync_client,
    select_model_family,
    build_system_message,
    build_user_message,
    configure_completion_kwargs,
)
from model_models import (
    TranslateRequest,
    TranslateResponse,
    extract_text_from_openai_response,
    extract_token_usage,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODEL_FAMILY = "gpt-4o"


def build_translation_instruction(request: TranslateRequest) -> str:
    """Build the system instruction for translation."""
    src = request.source_language or "the source language"
    return (
        f"You are a professional translator powered by OpenAI's {OPENAI_MODEL_FAMILY} model family. "
        f"Translate the provided text from {src} to {request.target_language}. "
        f"Preserve the original tone, style, and formatting. "
        f"Return ONLY the translated text, no explanations."
    )


def translate_result(
    request: TranslateRequest,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> TranslateResponse:
    """
    Translate generated model output using OpenAI GPT-4o hosted LLM.

    Args:
        request: TranslateRequest with text and target language.
        model: Optional explicit OpenAI model identifier.
        temperature: Sampling temperature (lower for consistent translation).

    Returns:
        TranslateResponse containing translated text and metadata.
    """
    selected_model = model or select_model_family("translate")

    system_msg = build_system_message(build_translation_instruction(request))
    user_msg = build_user_message(request.text)

    client = get_sync_client()

    kwargs = configure_completion_kwargs(
        messages=[system_msg, user_msg],
        model=selected_model,
        temperature=temperature,
        max_tokens=4096,
    )

    completion = client.chat.completions.create(**kwargs)

    translated = extract_text_from_openai_response(completion).strip()
    usage = extract_token_usage(completion)

    return TranslateResponse(
        translated_text=translated,
        source_language=request.source_language or "auto",
        target_language=request.target_language,
        model_used=selected_model,
    )


if __name__ == "__main__":
    sample = TranslateRequest(
        text="Hello, how are you today?",
        target_language="es",
        source_language="en",
    )
    result = translate_result(sample)
    print(f"Model: {result.model_used}")
    print(f"Translation: {result.translated_text}")
