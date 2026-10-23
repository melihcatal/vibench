import os
from typing import Dict, Optional
from cohere import Client as CohereClient
from object_metadata import IBMCloudObjectMetadataReader
from stored_document_ocr import GoogleDocumentAIOCR


class CohereMetadataEmbedder:
    """
    Embeds object metadata and extracted text for search using Cohere.
    """

    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key not configured.")

        self.cohere_client = CohereClient(api_key=self.api_key)
        self.metadata_reader = IBMCloudObjectMetadataReader()
        self.ocr_service = GoogleDocumentAIOCR()

    def embed_metadata_and_text(
        self, bucket_name: str, object_key: str, mime_type: Optional[str] = None
    ) -> Dict[str, list]:
        """
        Embeds metadata and extracted text from a document in IBM COS.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            mime_type: MIME type of the document.

        Returns:
            Dict[str, list]: Embeddings for metadata and text.
        """
        try:
            # Get object metadata
            metadata = self.metadata_reader.get_object_metadata(
                bucket_name=bucket_name, object_key=object_key
            )

            # Extract text using OCR
            text = self.ocr_service.process_document(
                bucket_name=bucket_name, object_key=object_key, mime_type=mime_type
            )

            # Generate embeddings
            metadata_text = " ".join(f"{k}: {v}" for k, v in metadata.items())
            combined_text = f"Metadata: {metadata_text}. Content: {text}"

            response = self.cohere_client.embed(
                texts=[combined_text], model="embed-english-v3.0"
            )

            return {
                "metadata": metadata,
                "text": text,
                "embedding": response.embeddings[0],
            }
        except Exception as e:
            raise Exception(f"Failed to embed metadata and text: {e}")
