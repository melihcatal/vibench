"""
result_translate.py - Translate generated model output.

Uses OpenAI's Chat Completions API (gpt-4o model) for high-quality text translation.
"""

from model_client import get_openai_client, select_model, build_chat_messages
from model_models import TranslationResult


def translate_text(
    text: str,
    target_language: str,
    source_language: str = "auto",
    model_family: str = "gpt-4o",
    temperature: float = 0.2,
) -> TranslationResult:
    """
    Translate model output text using OpenAI's hosted LLM.

    Args:
        text: The text to translate.
        target_language: Target language name (e.g. "Spanish", "French", "Japanese").
        source_language: Source language name, or "auto" for auto-detection.
        model_family: OpenAI model family (e.g. "gpt-4o").
        temperature: Sampling temperature (kept low for consistent translation).

    Returns:
        TranslationResult with translated text and metadata.
    """
    client = get_openai_client()
    model_id = select_model(model_family)

    if source_language == "auto":
        source_desc = "Detect the language automatically"
    else:
        source_desc = source_language

    system_prompt = (
        f"You are a professional translator powered by OpenAI. "
        f"Translate text from {source_desc} into {target_language}. "
        f"Preserve the original meaning, tone, and formatting. "
        f"Return ONLY the translated text with no explanations."
    )

    user_content = f"Translate the following text to {target_language}:\n\n{text}"

    messages = build_chat_messages(
        system_prompt=system_prompt,
        user_content=user_content,
    )

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=2048,
    )

    translated = ""
    if completion.choices and completion.choices[0].message:
        translated = completion.choices[0].message.content or ""

    return TranslationResult(
        translated_text=translated.strip(),
        source_language=source_language,
        target_language=target_language,
        model_used=model_id,
    )


def translate_batch(
    texts: list[str],
    target_language: str,
    source_language: str = "auto",
    model_family: str = "gpt-4o",
) -> list[TranslationResult]:
    """
    Translate multiple texts sequentially using OpenAI.

    Args:
        texts: List of texts to translate.
        target_language: Target language.
        source_language: Source language or "auto".
        model_family: OpenAI model family.

    Returns:
        List of TranslationResult objects.
    """
    results = []
    for text in texts:
        result = translate_text(text, target_language, source_language, model_family)
        results.append(result)
    return results


def translate_and_format(
    text: str,
    target_language: str,
    format_instruction: str = "",
    model_family: str = "gpt-4o",
) -> TranslationResult:
    """
    Translate text with additional formatting instructions.

    Args:
        text: The text to translate.
        target_language: Target language.
        format_instruction: Additional formatting requirements.
        model_family: OpenAI model family.

    Returns:
        TranslationResult with formatted translated text.
    """
    client = get_openai_client()
    model_id = select_model(model_family)

    format_part = f"\n\nAdditional formatting: {format_instruction}" if format_instruction else ""

    system_prompt = (
        f"You are a professional translator powered by OpenAI. "
        f"Translate text into {target_language}. Preserve meaning, tone, and structure.{format_part} "
        f"Return ONLY the translated text."
    )

    user_content = f"Translate the following text to {target_language}:\n\n{text}"

    messages = build_chat_messages(
        system_prompt=system_prompt,
        user_content=user_content,
    )

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
    )

    translated = ""
    if completion.choices and completion.choices[0].message:
        translated = completion.choices[0].message.content or ""

    return TranslationResult(
        translated_text=translated.strip(),
        source_language="auto",
        target_language=target_language,
        model_used=model_id,
    )


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog. This is a classic pangram."
    result = translate_text(sample, target_language="Spanish", model_family="gpt-4o")
    print(f"Source: {result.source_language}")
    print(f"Target: {result.target_language}")
    print(f"Model: {result.model_used}")
    print(f"Translation: {result.translated_text}")
