import os


def get_document_client(service):
    if service == "mindee":
        from mindee import Client

        return Client(api_key=os.getenv("MINDEE_API_KEY"))
    elif service == "google_documentai":
        from google.cloud import documentai_v1 as documentai

        return documentai.DocumentProcessorServiceClient(
            credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
