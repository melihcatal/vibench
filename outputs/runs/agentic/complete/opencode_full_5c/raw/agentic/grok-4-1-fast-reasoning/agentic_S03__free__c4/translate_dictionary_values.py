from typing import Dict, Any, Optional
from translation_client import get_translator

def translate_dictionary_values(
    dictionary: Dict[str, Any],
    source_lang: Optional[str] = None,
    target_lang: str
) -> Dict[str, Any]:
    translator = get_translator()
    def translate_if_string(value: Any) -> Any:
        if isinstance(value, str):
            return translator.translate_text(value, source_lang=source_lang, target_lang=target_lang).text
        return value
    return {key: translate_if_string(value) for key, value in dictionary.items()}