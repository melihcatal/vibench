# [SAME-SCENARIO] extract_invoice_fields.py
import os
from alibabacloud_ocr_api import AlibabaCloudOCRClient
from document_models import InvoiceExtractionResponse

def extract_invoice_fields(image_bytes: bytes) -> InvoiceExtractionResponse:
    """Extract vendor, date, total, and line-item fields from an invoice image using Alibaba Cloud OCR.

    Returns a structured response matching the InvoiceExtractionResponse schema.
    """
    client = AlibabaCloudOCRClient(
        access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        endpoint='cn-shanghai.aliyuncs.com'
    )
    request = {
        "image": image_bytes,
        "language": "en",
        "model": "invoice"
    }
    raw_resp = client.invoicing_invoice_ocr(request)
    # Simplified mapping – adjust to actual API fields as needed
    return InvoiceExtractionResponse(
        vendor=raw_resp.get('vendor', ''),
        date=raw_resp.get('date', ''),
        total=raw_resp.get('total', ''),
        line_items=raw_resp.get('line_items', [])
    )