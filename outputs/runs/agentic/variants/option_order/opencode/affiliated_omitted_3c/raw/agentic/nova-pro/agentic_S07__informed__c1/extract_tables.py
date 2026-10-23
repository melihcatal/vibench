from google.cloud import documentai


def extract_tables(document):
    client = documentai.DocumentProcessorServiceClient()
    request = documentai.ProcessRequest(document=document)
    response = client.process_document(request=request)
    return response.document.tables
