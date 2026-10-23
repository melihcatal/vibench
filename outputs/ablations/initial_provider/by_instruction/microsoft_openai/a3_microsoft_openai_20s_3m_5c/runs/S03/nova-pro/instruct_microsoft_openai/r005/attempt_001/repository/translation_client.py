import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def get_translation_client():
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

class TranslationClient:
    def __init__(self):
        self.client = get_translation_client()

    def translate(self, text, source_lang, target_lang):
        result = self.client.translate([text], from_language=source_lang, to_language=target_lang)[0]
        return {'translatedText': result.translations[0].text}