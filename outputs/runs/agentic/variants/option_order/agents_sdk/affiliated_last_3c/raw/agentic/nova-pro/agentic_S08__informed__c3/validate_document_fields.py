import alibabacloud_ocr_api

ALIBABA_CLOUD_ACCESS_KEY_ID = 'your_access_key_id'
ALIBABA_CLOUD_ACCESS_KEY_SECRET = 'your_secret_access_key'

def validate_document_fields(document_path):
    client = alibabacloud_ocr_api.Client(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
    response = client.invoice_recognition(document_path)
    # Validate fields from response
    return validated_fields