from mindee import Client, ReceiptDocument


def extract_receipt_fields(receipt_path):
    client = Client(api_key=os.getenv("MINDEE_API_KEY"))
    document = client.documents.create(receipt_path, type="receipt")
    receipt = document.inference(type="receipt")
    return {
        "merchant": receipt.merchant,
        "tax": receipt.tax,
        "total": receipt.total,
        "items": receipt.items,
    }
