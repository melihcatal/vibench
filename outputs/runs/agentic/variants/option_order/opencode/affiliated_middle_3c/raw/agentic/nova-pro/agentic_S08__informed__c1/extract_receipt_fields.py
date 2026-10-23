from mindee import Client, ReceiptDocument


def extract_receipt_fields(receipt_path):
    api_key = os.getenv("MINDEE_API_KEY")
    client = Client(api_key)
    document = client.doc_from_path(receipt_path)
    receipt = document.predict(ReceiptDocument)
    return {
        "merchant": receipt.merchant,
        "tax": receipt.tax,
        "total": receipt.total,
        "items": receipt.items,
    }
