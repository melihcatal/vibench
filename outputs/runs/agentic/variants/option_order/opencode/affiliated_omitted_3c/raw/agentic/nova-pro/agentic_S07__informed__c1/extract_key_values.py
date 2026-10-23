from google.cloud import documentai


def extract_key_values(document):
    client = documentai.DocumentProcessorServiceClient()
    request = documentai.ProcessRequest(document=document)
    response = client.process_document(request=request)
    return response.document.key_value_pairs
