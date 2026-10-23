from typing import Optional, List, Dict
from openai import OpenAI
from openai.types.chat import ChatCompletion
from model_client import create_openai_client, get_default_model
from model_models import (
    LocalizationResult,
    Message,
    ModelRole,
    normalize_messages,
)


LOCALE_NAMES: Dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ar": "Arabic",
    "ru": "Russian",
    "hi": "Hindi",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
}


def build_translation_prompt(
    text: str,
    source_locale: str,
    target_locale: str,
    context: Optional[str] = None,
) -> str:
    source_name = LOCALE_NAMES.get(source_locale, source_locale)
    target_name = LOCALE_NAMES.get(target_locale, target_locale)
    prompt = f"Translate the following text from {source_name} to {target_name}. Preserve the original formatting, tone, and meaning.\n\n"
    if context:
        prompt += f"Context: {context}\n\n"
    prompt += f"Text to translate:\n{text}"
    return prompt


def localize_platform_output(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    model: Optional[str] = None,
    context: Optional[str] = None,
    client: Optional[OpenAI] = None,
    temperature: float = 0.3,
) -> LocalizationResult:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    translation_prompt = build_translation_prompt(
        text, source_locale, target_locale, context
    )
    messages = [
        Message(
            role=ModelRole.SYSTEM,
            content="You are a professional translator. Provide only the translated text without explanations or notes.",
        ),
        Message(role=ModelRole.USER, content=translation_prompt),
    ]
    payload = {
        "model": target_model,
        "messages": [{"role": m.role.value, "content": m.content} for m in messages],
        "temperature": temperature,
    }
    response: ChatCompletion = client.chat.completions.create(**payload)
    choice = response.choices[0]
    translated_text = choice.message.content if choice.message.content else ""
    usage = response.usage
    return LocalizationResult(
        translated_text=translated_text,
        source_locale=source_locale,
        target_locale=target_locale,
        model=response.model,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        request_id=response.id,
        raw_response=response,
    )


def localize_batch(
    texts: List[str],
    target_locale: str,
    source_locale: str = "en",
    model: Optional[str] = None,
    context: Optional[str] = None,
    client: Optional[OpenAI] = None,
    temperature: float = 0.3,
) -> List[LocalizationResult]:
    if client is None:
        client = create_openai_client()
    results = []
    for text in texts:
        result = localize_platform_output(
            text=text,
            target_locale=target_locale,
            source_locale=source_locale,
            model=model,
            context=context,
            client=client,
            temperature=temperature,
        )
        results.append(result)
    return results


def detect_locale(
    text: str,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> str:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    prompt = (
        "Detect the language/locale of the following text. "
        "Respond with only the ISO 639-1 language code (e.g., en, es, fr, de, ja, zh, ko, ar, ru, hi, pt, it, nl).\n\n"
        f"Text: {text}"
    )
    messages = [
        Message(
            role=ModelRole.SYSTEM,
            content="You are a language detection expert. Respond with only the language code.",
        ),
        Message(role=ModelRole.USER, content=prompt),
    ]
    payload = {
        "model": target_model,
        "messages": [{"role": m.role.value, "content": m.content} for m in messages],
        "temperature": 0.0,
        "max_tokens": 10,
    }
    response: ChatCompletion = client.chat.completions.create(**payload)
    detected = response.choices[0].message.content or "en"
    return detected.strip().lower()
