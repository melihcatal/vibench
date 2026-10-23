from typing import Dict, List, Optional
import os
from mindee import Client, documents
from mindee.input import LocalInputSource
from .document_models import OCRResponse, OCRTextBlock


class MindeeDocumentClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise ValueError("MINDEE_API_KEY environment variable not set")
        self.client = Client(api_key=self.api_key)

    def extract_text_from_image(self, file_path: str) -> OCRResponse:
        input_source = LocalInputSource(file_path)
        response = self.client.parse(
            document_type=documents.TypeDocumentFile, input_source=input_source
        )
        return self._normalize_response(response)

    def _normalize_response(self, response) -> OCRResponse:
        blocks = []
        for page in response.document.inference.pages:
            for block in page.words:
                blocks.append(
                    OCRTextBlock(
                        text=block.value,
                        bounding_box={
                            "x1": block.bounding_box[0][0],
                            "y1": block.bounding_box[0][1],
                            "x2": block.bounding_box[2][0],
                            "y2": block.bounding_box[2][1],
                        },
                        confidence=block.confidence,
                    )
                )
        return OCRResponse(
            blocks=blocks, full_text=response.document.inference.full_text
        )
