from google.cloud import vision
from google.cloud import documentai_v1 as documentai

class DocumentClients:
    """Provides initialized clients for Google Cloud Vision and Document AI."""

    _vision_client = None
    _documentai_client = None

    @classmethod
    def get_vision_client(cls) -> vision.ImageAnnotatorClient:
        """Returns a singleton Google Cloud Vision API client."""
        if cls._vision_client is None:
            cls._vision_client = vision.ImageAnnotatorClient()
        return cls._vision_client

    @classmethod
    def get_documentai_client(cls) -> documentai.DocumentProcessorServiceClient:
        """Returns a singleton Google Cloud Document AI API client."""
        if cls._documentai_client is None:
            cls._documentai_client = documentai.DocumentProcessorServiceClient()
        return cls._documentai_client

# Example usage:
# vision_client = DocumentClients.get_vision_client()
# docai_client = DocumentClients.get_documentai_client()
