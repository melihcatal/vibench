from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse
import re

endpoint = 'https://api.cognitive.microsofttranslator.com'
key = 'your-azure-key'

client = TranslationClient(endpoint, key)

def translate_markup(source_language: str, target_language: str, markup: str) -> str:
    tag_pattern = re.compile(r'<[^>]+>')
    tags = tag_pattern.findall(markup)
    content = re.sub(tag_pattern, '', markup)
    request = TranslationRequest(source_language, target_language, content)
    response = client.translate(request.source_language, request.target_language, request.content)
    translated_content = TranslationResponse(response).translated_content
    translated_markup = translated_content
    for tag in tags:
        translated_markup = translated_markup.replace(content, tag, 1)
        content = content[len(tag):]
    return translated_markup