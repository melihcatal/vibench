from google.cloud import documentai

def extract_receipt_fields(document_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(document_path, 'rb') as document:
        document = document.read()
    response = client.process_document(document=document)
    return response