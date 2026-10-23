# provider: Google Cloud Translation API

from google.cloud import translate_v2 as translate
from document_models import InvoiceFieldsResponse, TranslationResult
from typing import Optional

TRANSLATOR = translate.Client()

SUPPORTED_TARGETS = ["es", "fr", "de", "zh"]


def translate_invoice_notes(
    extracted: InvoiceFieldsResponse, target_lang: str = "es"
) -> InvoiceFieldsResponse:
    """Translate vendor/memo fields into a target language while preserving original text."""
    if not extracted.vendor:
        return extracted  # nothing to translate

    if target_lang not in SUPPORTED_TARGETS:
        raise ValueError(
            f"Target language {target_lang} not supported. Choose from {SUPPORTED_TARGETS}"
        )

    result = TRANSLATOR.translate(extracted.vendor, target_language=target_lang)
    return InvoiceFieldsResponse(
        **extracted.dict(),
        vendor=extracted.vendor,  # keep original as source_text
        translated_vendor=result.get("translatedText"),
        translation=TranslationResult(
            source_text=extracted.vendor,
            target_text=result.get("translatedText"),
            source_language="en",
            target_language=target_lang,
        ),
    )


if __name__ == "__main__":
    # Demo translation using a dummy extracted invoice
    demo = InvoiceFieldsResponse(
        vendor="Invoice for services rendered",
        date="2024-07-10",
        total="$120.00",
        line_items=[],
        overall_confidence="high",
    )
    translated = translate_invoice_notes(demo, target_lang="fr")
    print("Translated invoice notes:")
    print(translated.json(indent=2))
