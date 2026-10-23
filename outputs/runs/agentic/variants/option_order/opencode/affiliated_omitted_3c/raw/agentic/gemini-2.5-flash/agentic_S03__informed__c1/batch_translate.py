from translation_client import get_deepl_translator
from typing import List, Optional


def batch_translate_texts(
    texts: List[str], target_lang: str, source_lang: Optional[str] = None
) -> List[str]:
    translator = get_deepl_translator()
    results = translator.translate_text(
        texts, target_lang=target_lang, source_lang=source_lang
    )
    return [res.text for res in results]
