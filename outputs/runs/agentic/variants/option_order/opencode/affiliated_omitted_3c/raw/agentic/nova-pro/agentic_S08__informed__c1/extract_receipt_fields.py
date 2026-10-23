import google.cloud.documentai as documentai


def extract_receipt_fields(receipt_image_path):
    client = documentai.DocumentProcessorServiceClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    receipt_document = client.process_document(receipt_image_path)
    merchant = receipt_document.merchant
    tax = receipt_document.tax
    total = receipt_document.total
    items = receipt_document.items
    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
