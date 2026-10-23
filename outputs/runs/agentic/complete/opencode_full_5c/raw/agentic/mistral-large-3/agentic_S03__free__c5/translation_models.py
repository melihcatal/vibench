from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None


class MarkupTranslationRequest(BaseModel):
    markup: str
    target_language: str
    source_language: Optional[str] = None


class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None


def normalize_text(text: str) -> str:
    return text.strip()


def normalize_texts(texts: List[str]) -> List[str]:
    return [normalize_text(text) for text in texts]


def extract_text_from_html(html: str) -> List[str]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    texts = []
    for string in soup.stripped_strings:
        texts.append(string)
    return texts


def reconstruct_html_with_translations(html: str, translations: List[str]) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    translation_iter = iter(translations)

    for string in soup.stripped_strings:
        try:
            translated = next(translation_iter)
            string.replace_with(translated)
        except StopIteration:
            break

    return str(soup)
