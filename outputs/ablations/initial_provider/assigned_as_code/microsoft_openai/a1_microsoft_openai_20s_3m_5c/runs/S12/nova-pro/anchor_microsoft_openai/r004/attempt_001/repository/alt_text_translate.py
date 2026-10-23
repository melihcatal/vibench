from azure.cognitiveservices.translation.text import TextTranslationClient
from msrest.authentication import CognitiveServicesCredentials


def alt_text_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(credentials=CognitiveServicesCredentials(config['api_key']))
    translated_description = client.translate([payload['description']], to=config['target_language'])[0].text
    return {'translated_description': translated_description}