import os
from openai import OpenAI
from document_client import load_config


def translate_invoice_notes(notes_text, target_language="English"):
    config = load_config()

    client = OpenAI(api_key=config["openai_api_key"])

    prompt = f"""Translate the following invoice notes to {target_language}:

Original notes: {notes_text}

Provide only the translation without any additional text or explanation."""

    response = client.chat.completions.create(
        model=config["openai_model"],
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator specializing in business and financial documents.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    translation = response.choices[0].message.content

    return {
        "original_text": notes_text,
        "translated_text": translation,
        "target_language": target_language,
        "translation_model": config["openai_model"],
        "character_count": len(notes_text),
    }
