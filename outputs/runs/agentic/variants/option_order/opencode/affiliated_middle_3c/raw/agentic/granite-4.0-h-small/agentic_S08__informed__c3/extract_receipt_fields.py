import aliyun_ocr_util as ocr


# Alibaba Cloud OCR invoice recognition (example SDK)
def extract_receipt_fields(file_path):
    # Detect merchant, tax, total, and items from receipt image
    result = ocr.recognize_receipt(file_path)
    receipt = {
        "merchant": result["merchant"],
        "tax": result["tax"],
        "total": result["total"],
        "items": result["items"],
    }
    return receipt
