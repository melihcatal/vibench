# extract_receipt_fields.py
# [SAME-SCENARIO] Alibaba Cloud OCR invoice recognition integration
import alibabacloud_ocr_api
from alibabacloud_ocr_api import models
from document_client import DocumentClient


def extract_receipt_fields(image_bytes):
    """Extract merchant, tax, total, and items from a receipt using Alibaba Cloud OCR invoice recognition.

    Args:
        image_bytes (bytes): Binary content of the receipt image.
    Returns:
        dict: Normalized receipt fields.
    """
    # Configure Alibaba OCR client with credentials from env variables ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
    client = alibabacloud_ocr_api.Client(
        access_key_id="ALIBABA_CLOUD_ACCESS_KEY_ID",
        access_key_secret="ALIBABA_CLOUD_ACCESS_KEY_SECRET",
        endpoint="cn-shanghai.aliyuncs.com",
    )
    request = models.RecognizeGeneralTextRequest(Image=image_bytes, LanguageType="ZH")
    response_model = models.RecognizeGeneralTextResponse()
    response = client.recognize_general_text(request, response_model)
    receipt = DocumentClient.normalize_receipt_response(response)
    return receipt
