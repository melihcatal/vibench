from bs4 import BeautifulSoup
from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    soup = BeautifulSoup(request.markup, 'html.parser')
    client = TranslationClient()

    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style'] and element.strip():
            translated_text = client.translate_text(
                text=str(element),
                target_language=request.target_language,
                source_language=request.source_language
            )
            element.replace_with(translated_text)

    return MarkupTranslationResponse(translated_markup=str(soup))