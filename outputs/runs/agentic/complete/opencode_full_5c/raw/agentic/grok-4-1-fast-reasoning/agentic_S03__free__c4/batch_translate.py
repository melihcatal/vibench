from typing import List, Optional
from translation_client import get_translator

def batch_translate(texts: List[str], source_lang: Optional[str] = None, target_lang: str) -> List[str]:
    translator = get_translator()
    return [
        translator.translate_text(text, source_lang=source_lang, target_lang=target_lang).text
        for text in texts
    ]