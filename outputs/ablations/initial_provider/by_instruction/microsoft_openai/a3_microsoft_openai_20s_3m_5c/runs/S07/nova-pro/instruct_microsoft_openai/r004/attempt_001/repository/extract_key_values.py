from.document_client import DocumentClient

def extract_key_values(image_path):
    client = DocumentClient(os.getenv('AZURE_VISION_ENDPOINT'), os.getenv('AZURE_VISION_KEY'))
    result = client.analyze_document(image_path, [TextDocumentFeatures.KEY_VALUE_PAIRS])
    return result.text_documents[0].key_value_pairs
