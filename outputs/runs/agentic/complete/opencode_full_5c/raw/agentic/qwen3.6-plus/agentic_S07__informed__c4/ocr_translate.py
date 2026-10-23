import os
from google.cloud import translate_v2 as translate
from document_models import OcrResult


GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")


def get_translate_client():
    return translate.Client()


def translate_text(
    text: str, target_language: str = "en", source_language: str = None
) -> str:
    client = get_translate_client()
    kwargs = {"q": text, "target": target_language}
    if source_language:
        kwargs["source"] = source_language
    result = client.translate(**kwargs)
    return result.get("translatedText", text)


def translate_ocr_result(
    result: OcrResult, target_language: str = "en", source_language: str = None
) -> OcrResult:
    translated_text = translate_text(result.full_text, target_language, source_language)
    translated_result = OcrResult(
        full_text=translated_text,
        page_count=result.page_count,
        confidence=result.confidence,
    )
    for seg in result.segments:
        if seg.text:
            translated_seg_text = translate_text(
                seg.text, target_language, source_language
            )
            translated_result.segments.append(seg)
            translated_result.segments[-1].text = translated_seg_text
    for elem in result.layout_elements:
        if elem.text:
            translated_elem_text = translate_text(
                elem.text, target_language, source_language
            )
            translated_result.layout_elements.append(elem)
            translated_result.layout_elements[-1].text = translated_elem_text
    return translated_result


def translate_text_batch(
    texts: list, target_language: str = "en", source_language: str = None
) -> list:
    client = get_translate_client()
    kwargs = {"q": texts, "target": target_language}
    if source_language:
        kwargs["source"] = source_language
    results = client.translate(**kwargs)
    return [r.get("translatedText", t) for r, t in zip(results, texts)]
