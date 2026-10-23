import re

from translation_client import get_translation_client, translate_with_client
from translation_models import normalize_payload


TAG_RE = re.compile(r"(<[^>]+>|[^<]+)")


def translate_markup(payload, config=None):
    payload = normalize_payload(payload)
    client = get_translation_client(config)
    parts = []
    for chunk in TAG_RE.findall(payload["markup"]):
        if chunk.startswith("<") and chunk.endswith(">"):
            parts.append(chunk)
        else:
            parts.append(
                translate_with_client(client, chunk, payload["source_language"], payload["target_language"])
            )
    return {
        "markup": "".join(parts),
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
