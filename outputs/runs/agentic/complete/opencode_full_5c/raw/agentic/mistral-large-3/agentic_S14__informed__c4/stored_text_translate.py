import os
from typing import Optional
from google.cloud import translate_v2 as translate
from stored_document_ocr import GoogleDocumentAIOCR


class GoogleCloudTranslationService:
    """
    Translates text extracted from a stored document using Google Cloud Translation.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("Google Cloud Translation credentials not configured.")

        self.client = translate.Client(project=self.project_id)
        self.ocr_service = GoogleDocumentAIOCR()

    def translate_text(
        self,
        bucket_name: str,
        object_key: str,
        target_language: str,
        mime_type: Optional[str] = None,
    ) -> str:
        """
        Translates text extracted from a document in IBM COS.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            target_language: Target language code (e.g., 'es', 'fr').
            mime_type: MIME type of the document.

        Returns:
            str: Translated text.
        """
        try:
            # Extract text using OCR
            text = self.ocr_service.process_document(
                bucket_name=bucket_name, object_key=object_key, mime_type=mime_type
            )

            # Translate the text
            result = self.client.translate(text, target_language=target_language)

            return result["translatedText"]
        except Exception as e:
            raise Exception(f"Failed to translate text: {e}")
