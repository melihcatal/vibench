from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.core.credentials import AzureKeyCredential

def batch_translate(texts, target_language):
    client = DocumentTranslationClient(endpoint="https://<your-translator-resource-name>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-translator-resource-key>"))
    inputs = [DocumentTranslationInput(source_url=f"memory://{i}", target_language_code=target_language) for i in range(len(texts))]
    poller = client.begin_translate_document(inputs)
    result = poller.result()
    return [r.target_document_url for r in result]