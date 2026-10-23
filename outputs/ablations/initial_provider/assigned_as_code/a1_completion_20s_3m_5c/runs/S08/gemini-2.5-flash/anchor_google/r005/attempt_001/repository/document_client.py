from google.cloud import documentai

def get_document_ai_client(location: str):
    return documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})

def get_processor_path(project_id: str, location: str, processor_id: str):
    client = documentai.DocumentProcessorServiceClient()
    return client.processor_path(project_id, location, processor_id)


class DocumentAIConfig:
    def __init__(self, project_id: str, location: str, invoice_processor_id: str, receipt_processor_id: str):
        self.project_id = project_id
        self.location = location
        self.invoice_processor_id = invoice_processor_id
        self.receipt_processor_id = receipt_processor_id