import os
from typing import Optional
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
}


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def translate_invoice_note(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    model: str = OPENAI_MODEL,
) -> str:
    client = get_openai_client()

    source_lang_name = SUPPORTED_LANGUAGES.get(source_language, "the source language")
    target_lang_name = SUPPORTED_LANGUAGES.get(target_language, "English")

    if source_language == "auto":
        system_prompt = f"You are a professional translator. Detect the language of the input text and translate it to {target_lang_name}. Preserve formatting and technical terms where appropriate."
    else:
        system_prompt = f"You are a professional translator. Translate the following text from {source_lang_name} to {target_lang_name}. Preserve formatting and technical terms where appropriate."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Translate this invoice note/description:\n\n{text}",
            },
        ],
        temperature=0.1,
        max_tokens=500,
    )

    return response.choices[0].message.content


def translate_invoice_notes_batch(
    notes: list,
    source_language: str = "auto",
    target_language: str = "en",
    model: str = OPENAI_MODEL,
) -> list:
    translations = []
    for note in notes:
        translated = translate_invoice_note(
            note, source_language, target_language, model
        )
        translations.append(
            {
                "original": note,
                "translated": translated,
                "source_language": source_language,
                "target_language": target_language,
                "model": model,
            }
        )
    return translations


def translate_invoice_description(
    invoice_data: dict, target_language: str = "en", model: str = OPENAI_MODEL
) -> dict:
    descriptions_to_translate = []

    line_items = invoice_data.get("line_items", [])
    for item in line_items:
        desc = item.get("description", "")
        if desc:
            descriptions_to_translate.append(desc)

    vendor_notes = invoice_data.get("vendor_notes", "")
    if vendor_notes:
        descriptions_to_translate.append(vendor_notes)

    if not descriptions_to_translate:
        return invoice_data

    translated_notes = translate_invoice_notes_batch(
        descriptions_to_translate, target_language=target_language, model=model
    )

    translated_invoice = invoice_data.copy()
    translated_line_items = []
    note_idx = 0

    for item in line_items:
        new_item = item.copy()
        if item.get("description") and note_idx < len(translated_notes):
            new_item["translated_description"] = translated_notes[note_idx][
                "translated"
            ]
            note_idx += 1
        translated_line_items.append(new_item)

    translated_invoice["line_items"] = translated_line_items

    if vendor_notes and note_idx < len(translated_notes):
        translated_invoice["translated_vendor_notes"] = translated_notes[note_idx][
            "translated"
        ]

    translated_invoice["translation_metadata"] = {
        "target_language": target_language,
        "model_used": model,
        "provider": "openai",
    }

    return translated_invoice
