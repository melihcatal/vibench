from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.ai.translation.document.models import InputDocument, TranslationTarget


def translate_secret_rotation_runbook(payload, config=None):
    config = config or {}
    endpoint = config['translation_endpoint']
    key = config['translation_key']
    credential = AzureKeyCredential(key)
    client = DocumentTranslationClient(endpoint=endpoint, credential=credential)
    input_document = InputDocument(document_url=payload['runbook_url'])
    target = TranslationTarget(language='es')
    input = DocumentTranslationInput(input_document, [target])
    poller = client.begin_translation(input)
    result = poller.result()
    return {'translated_runbook': result.documents[0].translated_document_url}