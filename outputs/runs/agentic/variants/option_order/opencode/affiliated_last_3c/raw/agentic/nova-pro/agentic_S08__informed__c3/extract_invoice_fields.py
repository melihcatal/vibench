from alibabacloud_ocr_api.client import Client as OCRClient
from alibabacloud_ocr20191230.models import RecognizeInvoiceRequest

import os

access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def extract_invoice_fields(image_path):
    client = OCRClient(access_key_id, access_key_secret)
    request = RecognizeInvoiceRequest()
    request.image_url = image_path
    response = client.recognize_invoice(request)
    return response.to_map()
