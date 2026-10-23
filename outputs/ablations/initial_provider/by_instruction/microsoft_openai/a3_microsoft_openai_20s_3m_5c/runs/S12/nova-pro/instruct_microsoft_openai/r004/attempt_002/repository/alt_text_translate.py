from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_text(text, target_language):
    endpoint = os.getenv('TRANSLATION_ENDPOINT')
    key = os.getenv('TRANSLATION_KEY')
    credential = AzureKeyCredential(key)
    client = DocumentTranslationClient(endpoint, credential)
    result = client.translate(text, target_language)
    return result.translations[0].text