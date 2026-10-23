from alibabacloud_ocr_api import AlibabaCloudOCRClient


def extract_invoice_fields(invoice_image):
    client = AlibabaCloudOCRClient(
        ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
    )
    response = client.recognize_invoice(invoice_image)
    return response
