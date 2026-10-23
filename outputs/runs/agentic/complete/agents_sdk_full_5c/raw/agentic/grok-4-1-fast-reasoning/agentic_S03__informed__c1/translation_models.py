from typing import List
from deepl import TextResult

def normalize_texts(texts: List[str]) -> List[str]:
    """Normalize input texts by stripping whitespace."""
    return [text.strip() for text in texts]

def extract_translated_texts(results: List[TextResult]) -> List[str]:
    """Extract translated text from DeepL results."""
    return [result.text for result in results]

def normalize_single_text(text: str) -> str:
    """Normalize single text."""
    return text.strip()