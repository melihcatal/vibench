from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.core.credentials import AzureKeyCredential

class TranslationClient:
    def __init__(self, endpoint, key):
        self.client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

    def translate(self, source_language, target_language, content):
        input = DocumentTranslationInput(
            source_url=None,
            target_url=None,
            source_language_code=source_language,
            target_language_codes=[target_language],
            document_type='plain'
        )
        poller = self.client.begin_translation(input)
        result = poller.result()
        return result.translations[0].content