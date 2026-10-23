from model_client import HostedLLMClient
from model_models import (
    LLMRequest,
    ModelConfig,
    TranslationRequest,
    TranslationResponse,
    normalize_messages,
)


SYSTEM_PROMPT_TEMPLATE = (
    "You are a professional translator. Translate the following text from {source_lang} to {target_lang}. "
    "Preserve the tone, style, and formatting of the original. "
    "Return only the translated text without explanations or notes."
)


def translate_text(
    text: str,
    target_language: str,
    source_language: str = "auto",
    model: str = "gpt-4o",
    temperature: float = 0.3,
    config: ModelConfig | None = None,
) -> TranslationResponse:
    client = HostedLLMClient(config=config)
    detected_source = (
        source_language if source_language != "auto" else "the source language"
    )
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        source_lang=detected_source,
        target_lang=target_language,
    )
    user_content = f"Translate the following text:\n\n{text}"
    messages = normalize_messages(user_content, system_prompt=system_prompt)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
    )
    response = client.chat_completion(request)
    return TranslationResponse(
        translated_text=response.content,
        source_language=source_language,
        target_language=target_language,
        model=model,
    )


def translate_batch(
    texts: list[str],
    target_language: str,
    source_language: str = "auto",
    model: str = "gpt-4o",
    temperature: float = 0.3,
    config: ModelConfig | None = None,
) -> list[TranslationResponse]:
    return [
        translate_text(
            text, target_language, source_language, model, temperature, config
        )
        for text in texts
    ]


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    result = translate_text(
        sample, target_language="Spanish", source_language="English"
    )
    print(f"Original: {sample}")
    print(f"Translation: {result.translated_text}")
    print(f"Model: {result.model}")
