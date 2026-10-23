from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_text(text, target_language):
    client = DocumentTranslationClient(endpoint='https://<your-resource-name>.cognitiveservices.azure.com/', credential=AzureKeyCredential('<your-api-key>'))
    result = client.translate(text, target_language)
    return result
