from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, normalize_response
import re

async def translate_markup(markup, target_language):
    def replace_text(match):
        text = match.group(1)
        translated_text = await translate_text(text, target_language)
        return match.group(0).replace(text, translated_text.translated_text)
    pattern = re.compile(r'>(.*?)<')
    translated_markup = pattern.sub(replace_text, markup)
    return translated_markup