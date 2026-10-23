import os
import re
from deepl import Translator
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse
from translation_client import get_deepl_client, normalize_language_code


def _split_by_tags(html_content: str):
    segments = []
    pattern = re.compile(r"(<[^>]+>|[^<]+)")
    for match in pattern.finditer(html_content):
        token = match.group(0)
        if token.startswith("<"):
            segments.append(("tag", token))
        else:
            stripped = token.strip()
            if stripped:
                segments.append(("text", token))
            else:
                segments.append(("whitespace", token))
    return segments


def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)

    segments = _split_by_tags(request.html_content)
    text_segments = [seg for seg in segments if seg[0] == "text"]

    if not text_segments:
        return MarkupTranslationResponse(
            translated_markup=request.html_content,
            source_lang=request.source_lang,
            target_lang=target_lang,
        )

    texts_to_translate = [seg[1] for seg in text_segments]

    results = client.translate_text(
        texts_to_translate,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang,
        tag_handling="html",
    )

    translated_index = 0
    output_parts = []
    for seg_type, seg_value in segments:
        if seg_type == "text":
            output_parts.append(results[translated_index].text)
            translated_index += 1
        else:
            output_parts.append(seg_value)

    translated_markup = "".join(output_parts)

    return MarkupTranslationResponse(
        translated_markup=translated_markup,
        source_lang=request.source_lang,
        target_lang=target_lang,
    )


if __name__ == "__main__":
    req = MarkupTranslationRequest(
        html_content="<p>Hello <strong>world</strong></p>",
        source_lang="en",
        target_lang="de",
    )
    resp = translate_markup(req)
    print(resp.translated_markup)
