from azure.ai.translation.document import DocumentTranslationClient

class TranslationClient:
    def __init__(self, endpoint, key):
        self.client = DocumentTranslationClient(endpoint, key)

    def translate(self, source_text, target_language):
        result = self.client.translate(source_text, target_language)
        return result.translations[0].text