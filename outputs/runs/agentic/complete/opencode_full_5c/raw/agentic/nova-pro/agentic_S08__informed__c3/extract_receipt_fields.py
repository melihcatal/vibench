import alibabacloud_ocr_api


def extract_receipt_fields(document_path):
    client = alibabacloud_ocr_api.Client(
        access_key_id="your-access-key-id", access_key_secret="your-access-key-secret"
    )
    response = client.recognize_receipt(document_path)
    return response
