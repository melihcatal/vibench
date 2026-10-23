from alibabacloud_ocr_api import Client as OcrClient

def extract_receipt_fields(document):
    ocr_client = OcrClient()
    response = ocr_client.invoice_recognition(document)
    # Extract fields from response