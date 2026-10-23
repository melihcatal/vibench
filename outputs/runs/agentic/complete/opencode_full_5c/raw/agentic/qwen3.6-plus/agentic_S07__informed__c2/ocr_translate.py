import os
from typing import List, Optional
import deepl
from document_models import DocumentTextResult


DEEPL_API_URL = "https://api-free.deepl.com"
DEEPL_TARGET_LANG = os.environ.get("DEEPL_TARGET_LANG", "EN")


def translate_ocr_text(
    ocr_result: DocumentTextResult,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> DocumentTextResult:
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    target = target_lang or DEEPL_TARGET_LANG

    translator = deepl.Translator(deepl_auth_key, server_url=DEEPL_API_URL)

    translated_lines = []
    for line in ocr_result.lines:
        if line.text.strip():
            result = translator.translate_text(
                line.text,
                source_lang=source_lang,
                target_lang=target,
            )
            translated_words = []
            for word in line.words:
                translated_words.append(word)
            translated_lines.append(
                type(line)(
                    words=translated_words,
                )
            )
        else:
            translated_lines.append(line)

    full_text = "\n".join(l.text for l in translated_lines)
    translated_result = translator.translate_text(
        ocr_result.raw_text,
        source_lang=source_lang,
        target_lang=target,
    )

    return DocumentTextResult(
        raw_text=translated_result.text,
        lines=translated_lines,
        confidence=ocr_result.confidence,
        page_count=ocr_result.page_count,
    )


def translate_text_list(
    texts: List[str],
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> List[str]:
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    target = target_lang or DEEPL_TARGET_LANG

    translator = deepl.Translator(deepl_auth_key, server_url=DEEPL_API_URL)

    results = translator.translate_text(
        texts,
        source_lang=source_lang,
        target_lang=target,
    )

    return [r.text for r in results]


if __name__ == "__main__":
    sample_result = DocumentTextResult(
        raw_text="Bonjour le monde",
        lines=[],
        confidence=1.0,
    )
    translated = translate_ocr_text(sample_result, target_lang="EN")
    print(translated.raw_text)
