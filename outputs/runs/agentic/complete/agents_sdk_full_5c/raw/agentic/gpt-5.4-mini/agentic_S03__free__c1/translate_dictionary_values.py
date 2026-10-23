from typing import Any, Dict

from translation_client import load_config, post_translate
from translation_models import rebuild_dictionary


def translate_dictionary_values(values: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
    texts = ["" if v is None else str(v) for v in values.values()]
    cfg = load_config()
    data = post_translate({"text": texts, "source_lang": source_lang, "target_lang": target_lang}, cfg)
    translated = [item["text"] for item in data["translations"]]
    return rebuild_dictionary(translated, values)
