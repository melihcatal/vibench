import os
from azure.core.exceptions import AzureError
from azure.ai.formrecognizer import DocumentAnalysisClient
from document_models import OCRResponse

class DocumentClient:
    def __init__(self):
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        credential = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        if not endpoint or not credential:
            raise RuntimeError("Azure Form Recognizer credentials missing")
        self.client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)

    def extract_text(self, image_path: str) -> dict:
        # Call provider API and return raw JSON payload
        poller = self.client.begin_analyze_document("prebuilt/read", image_path)
        result = poller.result()
        # Normalize to our internal OCRResponse shape
        blocks = [
            {
                "page": 1,
                "text": line.text,
                "bbox": line.bounding_box,
                "type": "line"
            }
            for line in result.lines
        ]
        return {
            "blocks": blocks,
            "raw_response": result.raw_response.json()
        }
