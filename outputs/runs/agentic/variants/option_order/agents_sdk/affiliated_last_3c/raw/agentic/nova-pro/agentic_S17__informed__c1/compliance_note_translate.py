from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput

def translate_compliance_note(text, target_language):
    client = DocumentTranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=azure.identity.DefaultAzureCredential())
    input = DocumentTranslationInput(source_url='https://example.com/source.txt', target_url='https://example.com/target.txt', target_language_code=target_language)
    poller = client.begin_translate_document(input)
    result = poller.result()
    return result.target_document_url