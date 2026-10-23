from.document_client import DocumentClient

def extract_text(image_path):
    client = DocumentClient(os.getenv('AZURE_VISION_ENDPOINT'), os.getenv('AZURE_VISION_KEY'))
    result = client.analyze_document(image_path, [TextDocumentFeatures.TEXT])
    return result.text_documents[0].text
