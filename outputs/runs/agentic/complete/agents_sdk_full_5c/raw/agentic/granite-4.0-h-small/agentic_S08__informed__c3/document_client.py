import os
from dataclasses import dataclass
from document_models import InvoiceExtractionRequest, ReceiptExtractionRequest

@dataclass
class DocumentClientConfig:
    # AWS credentials for Textract (used in extract_invoice_fields.py)
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    # Optional endpoint override for testing (e.g., localstack)
    TextractEndpointURL: str | None = os.getenv("TextractEndpointURL")
    
    # Mindee API key for receipt OCR
    MINDEE_API_KEY: str | None = os.getenv("MINDEE_API_KEY")
    
    # Google Cloud credentials for Document AI Invoice Processor (if used instead of Textract)
    GOOGLE_APPLICATION_CREDENTIALS: str | None = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    DocumentAI_ENDPOINT: str | None = os.getenv("DocumentAI_ENDPOINT")

@dataclass
class InvoiceExtractionClient:
    config: DocumentClientConfig
    
    def get_textract_response(self, file_path: str) -> InvoiceExtractionRequest:
        # placeholder that would invoke boto3 client configured above
        return InvoiceExtractionRequest(
            vendor="SAMPLE_VENDOR",
            date="2024-01-01",
            total=0.0,
            line_items=[]
        )

class ReceiptExtractionClient:
    def __init__(self, config: DocumentClientConfig):
        self.config = config
        try:
            # Attempt to import Mindee SDK lazily; raise ImportError if not installed
            from mindee import MindeeClient
            self.mindee_client = MindeeClient(api_key=self.config.MINDEE_API_KEY)
        except ImportError:
            raise ImportError("Mindee SDK not installed. Install via `pip install mindee`")
    
    def process_receipt(self, file_path: str) -> ReceiptExtractionRequest:
        with open(file_path, "rb") as f:
            result = self.mindee_client.invoice.process(f)
        # Build a simple request object (similar to the response models in document_models)
        receipt = ReceiptExtractionRequest(
            merchant=result.document.merchant.name if result.document.merchant else "",
            tax=result.document.parse.get("fields", []),
            total=result.document.parse.get("total", "0.0"),
            line_items=result.document.parse.get("items", [])
        )
        return receipt
