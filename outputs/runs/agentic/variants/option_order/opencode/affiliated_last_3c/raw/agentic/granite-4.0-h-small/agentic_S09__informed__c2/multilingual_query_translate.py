from translate import Translator
from typing import List

# Provider: Google Translate (via translate library)


def translate_query(query: str, target_language: str = "en") -> str:
    """Translate a query to target language before multilingual embedding search."""
    translator = Translator(to_lang=target_language)
    translation = translator.translate(query)
    return translation


def translate_batch(queries: List[str], target_language: str = "en") -> List[str]:
    """Batch translate queries.

    Example:
        >>> translate_batch(["Bonjour", "Hola"], target_language="en")
        ['Hello', 'Hi']
    """
    translator = Translator(to_lang=target_language)
    return [translator.translate(q) for q in queries]
