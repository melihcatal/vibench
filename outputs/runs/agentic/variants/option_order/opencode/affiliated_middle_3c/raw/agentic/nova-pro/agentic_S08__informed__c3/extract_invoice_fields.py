from alibabacloud_ocr_api import AlibabaCloudOcrApi


def extract_invoice_fields(invoice_image):
    api = AlibabaCloudOcrApi()
    result = api.extract_invoice(invoice_image)
    return result
