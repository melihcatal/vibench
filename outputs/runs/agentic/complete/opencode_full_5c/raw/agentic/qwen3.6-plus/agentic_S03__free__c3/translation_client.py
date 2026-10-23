import os
import json
from typing import Optional, Dict, Any, List
from openai import OpenAI
from translation_models import (
    TranslationRequest,
    TranslationResult,
    BatchTranslationRequest,
    BatchTranslationResult,
    MarkupTranslationRequest,
    DictionaryTranslationRequest,
    normalize_language_code,
    count_words,
    count_characters,
)

OPENAI_MODEL = "gpt-4o"
OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url=OPENAI_API_BASE)


def build_translation_system_prompt(
    target_language: str,
    preserve_formatting: bool = False,
    context: Optional[str] = None,
) -> str:
    prompt = f"You are a professional translator. Translate the provided text to {target_language}."
    if preserve_formatting:
        prompt += (
            " Preserve all formatting, line breaks, and special characters exactly."
        )
    if context:
        prompt += f" Context for translation: {context}"
    prompt += " Return only the translated text with no additional commentary."
    return prompt


def build_markup_translation_system_prompt(target_language: str) -> str:
    return (
        f"You are a professional translator specializing in markup preservation. "
        f"Translate the text content to {target_language} while preserving ALL HTML/XML/markdown tags, "
        f"attributes, and structural elements exactly as they appear. "
        f"Do not translate tag names, attribute names, or URLs. "
        f"Return only the translated markup with no additional commentary."
    )


def build_dictionary_translation_system_prompt(
    target_language: str, translate_keys: bool = False
) -> str:
    prompt = (
        f"You are a professional translator. Translate the dictionary values to {target_language}. "
        f"Preserve the JSON structure exactly. "
    )
    if translate_keys:
        prompt += "Translate both keys and values. "
    else:
        prompt += "Keep all keys unchanged and only translate the values. "
    prompt += "Return only the translated JSON object with no additional commentary."
    return prompt


def parse_translation_response(
    response_text: str, target_language: str, source_language: str
) -> TranslationResult:
    translated = response_text.strip()
    return TranslationResult(
        translated_text=translated,
        source_language_detected=source_language,
        target_language=target_language,
        confidence=1.0,
        character_count=count_characters(translated),
        word_count=count_words(translated),
    )


def translate_single_text(
    client: OpenAI, request: TranslationRequest
) -> TranslationResult:
    target_lang = normalize_language_code(request.target_language)
    source_lang = normalize_language_code(request.source_language)
    system_prompt = build_translation_system_prompt(
        target_lang,
        preserve_formatting=request.preserve_formatting,
        context=request.context,
    )
    if request.custom_instructions:
        system_prompt += f"\nAdditional instructions: {request.custom_instructions}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.text},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    translated_text = response.choices[0].message.content
    return parse_translation_response(translated_text, target_lang, source_lang)


def translate_batch_texts(
    client: OpenAI, request: BatchTranslationRequest
) -> BatchTranslationResult:
    target_lang = normalize_language_code(request.target_language)
    source_lang = normalize_language_code(request.source_language)
    system_prompt = build_translation_system_prompt(
        target_lang,
        preserve_formatting=request.preserve_formatting,
        context=request.context,
    )
    system_prompt += (
        "\n\nYou will receive a JSON array of strings. "
        "Return a JSON array of translated strings in the exact same order. "
        "Return only the JSON array with no additional text."
    )
    input_json = json.dumps(request.texts, ensure_ascii=False)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_json},
        ],
        temperature=0.3,
        max_tokens=8192,
    )
    translated_array = json.loads(response.choices[0].message.content.strip())

    results = []
    total_chars = 0
    total_words = 0
    for orig, trans in zip(request.texts, translated_array):
        result = parse_translation_response(trans, target_lang, source_lang)
        results.append(result)
        total_chars += result.character_count
        total_words += result.word_count

    return BatchTranslationResult(
        results=results, total_characters=total_chars, total_words=total_words
    )


def translate_markup_content(
    client: OpenAI, request: MarkupTranslationRequest
) -> TranslationResult:
    target_lang = normalize_language_code(request.target_language)
    source_lang = normalize_language_code(request.source_language)
    system_prompt = build_markup_translation_system_prompt(target_lang)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.markup},
        ],
        temperature=0.3,
        max_tokens=8192,
    )
    translated_markup = response.choices[0].message.content.strip()
    return parse_translation_response(translated_markup, target_lang, source_lang)


def translate_dictionary_content(
    client: OpenAI, request: DictionaryTranslationRequest
) -> Dict[str, Any]:
    target_lang = normalize_language_code(request.target_language)
    source_lang = normalize_language_code(request.source_language)
    system_prompt = build_dictionary_translation_system_prompt(
        target_lang, request.translate_keys
    )

    input_json = json.dumps(request.data, ensure_ascii=False)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_json},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    translated_json = json.loads(response.choices[0].message.content.strip())
    return translated_json
