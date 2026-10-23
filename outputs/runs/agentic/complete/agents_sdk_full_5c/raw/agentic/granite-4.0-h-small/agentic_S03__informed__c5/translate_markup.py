import os
import html
from translation_client import create_translator_client
from translation_models import TranslationResponse

def _unescape_html(text: str) -> str:
    """Restore HTML entities after translation to preserve markup.",
    return html.unescape(text)

def translate_markup(source_html: str, target_lang: str = "es") -> str:
    """Translate HTML/markup while preserving tag structure.",
    # Extract text nodes only for translation
    text_nodes = []
    unescaped_parts = []
    tag_buffer = []
    depth = 0
    i = 0
    while i < len(source_html):
        if source_html.startswith('<', i):
            if depth == 0:
                # accumulate preceding text
                text_nodes.append(''.join(tag_buffer))
                tag_buffer = []
            depth += 1
            tag_buffer.append(source_html[i])
        elif source_html.startswith('>', i):
            depth -= 1
            tag_buffer.append(source_html[i])
            if depth == 0:
                # flush tag as raw
                text_nodes.append(''.join(tag_buffer))
                tag_buffer = []
        else:
            tag_buffer.append(source_html[i])
        i += 1
    if tag_buffer:
        text_nodes.append(''.join(tag_buffer))

    # Translate each text node
    translated_nodes = []
    translator = create_translator_client()
    for node in text_nodes:
        if not node.strip():
            translated_nodes.append(node)
            continue
        resp = translator.translate(
            texts=[node],
            to_language=target_lang
        )
        translated = TranslationResponse(resp[0]).get_translated_text()
        translated_nodes.append(_unescape_html(translated))

    # Reassemble preserving original order
    result = ''
    node_idx = 0
    while node_idx < len(text_nodes):
        result += text_nodes[node_idx]
        node_idx += 1
    return result
