# [HELPER] document_client.py
import os
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Generic base class for any document extraction client
T = TypeVar('T')

class DocumentClient(ABC, Generic[T]):
    @abstractmethod
    def extract(self, image_bytes: bytes) -> T:
        """Extract structured data from image bytes; return typed response object."""
        pass

class AlibabaOCRClient(DocumentClient[InvoiceExtractionResponse]):
    def __init__(self):
        self.access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self.access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        self.endpoint = 'cn-shanghai.aliyuncs.com'
        # Initialize SDK client here (not shown for brevity)

    def extract(self, image_bytes: bytes) -> InvoiceExtractionResponse:
        # Call Alibaba Cloud OCR API
        # … mapping logic as in extract_invoice_fields.py ...
        raise NotImplementedError  # placeholder for actual SDK call

class MindeeClient(DocumentClient[ReceiptExtractionResponse]):
    def __init__(self):
        self.api_key = os.getenv('MINDEE_API_KEY')
        # Initialize SDK client here

    def extract(self, image_bytes: bytes) -> ReceiptExtractionResponse:
        # Call Mindee Invoice OCR API
        # … mapping logic as in extract_receipt_fields.py ...
        raise NotImplementedError