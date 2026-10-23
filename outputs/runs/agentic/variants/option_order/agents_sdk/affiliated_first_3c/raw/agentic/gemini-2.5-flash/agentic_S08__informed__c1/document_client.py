import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from mindee import Client as MindeeClient

class DocumentClients:
    """
    Provides helper utilities for initializing and configuring Structured Document Extraction clients.
    """

    @staticmethod
    def get_document_ai_client(location: str) -> documentai.DocumentProcessorServiceClient:
        """
        Initializes and returns a Google Cloud Document AI client.
        Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
        """
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        return client

    @staticmethod
    def get_mindee_client(api_key: Optional[str] = None) -> MindeeClient:
        """
        Initializes and returns a Mindee client.
        Requires MINDEE_API_KEY environment variable or direct API key.
        """
        if api_key is None:
            api_key = os.environ.get("MINDEE_API_KEY")
        if not api_key:
            raise ValueError("Mindee API key not provided and MINDEE_API_KEY environment variable not set.")
        return MindeeClient(api_key=api_key)

if __name__ == "__main__":
    # Example usage
    # document_ai_client = DocumentClients.get_document_ai_client(location="us")
    # print("Document AI client initialized:", document_ai_client)

    # mindee_client = DocumentClients.get_mindee_client(api_key="YOUR_MINDEE_API_KEY")
    # print("Mindee client initialized:", mindee_client)
    pass
