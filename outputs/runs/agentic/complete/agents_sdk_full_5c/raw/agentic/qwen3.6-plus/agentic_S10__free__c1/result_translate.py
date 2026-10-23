"""
result_translate.py — Translate generated model output to a target language.

Uses the OpenAI Chat Completions API (api.openai.com) with the
gpt-4o-2024-08-06 model for high-quality neural machine translation.
"""

from __future__ import annotations

from typing import Optional

from model_client import run_completion, resolve_model
from model_models import (
    TranslationRequest,
    CompletionResponse,
    build_chat_request,
)

# Concrete OpenAI model identifier for translation
TRANSLATION_MODEL = resolve_model("gpt-4o")  # gpt-4o-2024-08-06

TRANSLATION_SYSTEM_PROMPT = (
    "You are a professional translator. Translate the provided text into the "
    "specified target language. Preserve the original meaning, tone, and "
    "formatting. Output only the translated text with no additional commentary "
    "or explanation."
)


def translate_result(
    text: str,
    target_language: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> str:
    """
    Translate text using the hosted OpenAI gpt-4o model.

    Parameters
    ----------
    text : str
        Source text to translate.
    target_language : str
        Target language name (e.g., "Spanish", "French", "Japanese", "en").
    model : str, optional
        Concrete OpenAI model ID (defaults to gpt-4o-2024-08-06).
    temperature : float
        Sampling temperature.

    Returns
    -------
    str
        The translated text.
    """
    target_model = model or TRANSLATION_MODEL
    user_prompt = (
        f"Translate the following text into {target_language}:\n\n{text}"
    )
    request = build_chat_request(
        system_prompt=TRANSLATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=target_model,
        temperature=temperature,
    )
    response: CompletionResponse = run_completion(request)
    return response.content.strip()


def translate_batch(
    texts: list[str],
    target_language: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> list[str]:
    """
    Translate a list of texts using the hosted OpenAI gpt-4o model.

    Parameters
    ----------
    texts : list of str
        Source texts to translate.
    target_language : str
        Target language name.
    model : str, optional
        Concrete OpenAI model ID.
    temperature : float
        Sampling temperature.

    Returns
    -------
    list of str
        Translated texts in the same order as input.
    """
    translations: list[str] = []
    for text in texts:
        translations.append(
            translate_result(text, target_language, model=model, temperature=temperature)
        )
    return translations


def translate_structured(
    text: str,
    target_language: str,
    preserve_format: bool = True,
    model: Optional[str] = None,
) -> str:
    """
    Translate text while attempting to preserve formatting (lists, code, etc.).

    Parameters
    ----------
    text : str
        Source text.
    target_language : str
        Target language name.
    preserve_format : bool
        When True, instructs the model to keep structural formatting intact.
    model : str, optional
        Concrete OpenAI model ID.

    Returns
    -------
    str
        Translated text with formatting preserved where possible.
    """
    system_addition = ""
    if preserve_format:
        system_addition = (
            " Preserve all structural formatting including lists, headers, "
            "code blocks, and indentation. Translate only the natural-language "
            "content."
        )

    request = TranslationRequest(
        input_text=text,
        target_language=target_language,
        model=model or TRANSLATION_MODEL,
    )

    messages = request.to_chat_messages()
    messages[0].content += system_addition

    from model_models import CompletionRequest

    completion_request = CompletionRequest(
        messages=messages,
        model=model or TRANSLATION_MODEL,
        temperature=0.3,
    )
    response: CompletionResponse = run_completion(completion_request)
    return response.content.strip()


if __name__ == "__main__":
    sample = "The weather today is beautiful, with clear skies and warm sunshine."
    translated = translate_result(sample, "French")
    print(f"Original: {sample}")
    print(f"French:   {translated}")
