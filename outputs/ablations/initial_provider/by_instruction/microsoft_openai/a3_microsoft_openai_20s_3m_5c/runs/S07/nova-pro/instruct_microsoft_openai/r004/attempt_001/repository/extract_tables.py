from.document_client import DocumentClient

def extract_tables(image_path):
    client = DocumentClient(os.getenv('AZURE_VISION_ENDPOINT'), os.getenv('AZURE_VISION_KEY'))
    result = client.analyze_document(image_path, [TableDocumentFeatures.TABLES])
    return result.tables
