from __future__ import annotations

from deepl import Translator

from identity_models import ConsentText

DEEPL_SOURCE_LANG = "en"


def translate_consent_copy(consent: ConsentText) -> str:
    translator = Translator()
    result = translator.translate_text(
        consent.text,
        source_lang=consent.source_locale or DEEPL_SOURCE_LANG,
        target_lang=consent.target_locale,
    )
    return str(result)
