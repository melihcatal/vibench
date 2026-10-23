from google.cloud import documentai

def get_document_client(project_id, location):
    return documentai.DocumentProcessorServiceClient(project=project_id, location=location)