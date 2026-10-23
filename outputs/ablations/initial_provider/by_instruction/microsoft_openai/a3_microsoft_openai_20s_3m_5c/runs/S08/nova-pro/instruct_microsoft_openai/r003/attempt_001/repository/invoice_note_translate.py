from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_invoice_note(note: str, target_language: str):
    endpoint = os.getenv('TRANSLATION_ENDPOINT')
    key = os.getenv('TRANSLATION_KEY')
    credential = AzureKeyCredential(key)
    client = DocumentTranslationClient(endpoint, credential)
    poller = client.begin_translate_document(note, target_language)
    result = poller.result()
    return result[0]['translatedText']