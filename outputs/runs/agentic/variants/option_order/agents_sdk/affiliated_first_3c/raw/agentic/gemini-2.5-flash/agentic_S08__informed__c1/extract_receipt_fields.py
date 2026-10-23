import os
from mindee import Client, product

def extract_receipt_fields(api_key: str, file_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Mindee.
    """
    mindee_client = Client(api_key=api_key)

    # Load a file from disk and parse it.
    input_doc = mindee_client.doc_from_path(file_path)
    
    # Parse the document as a Financial Document (handles receipts and invoices)
    # Mindee's Financial Document product can process both, but we'll focus on receipt fields.
    result = mindee_client.parse(input_doc, product.ReceiptV5)

    extracted_data = {
        "merchant_name": "",
        "total_amount": None,
        "tax_amount": None,
        "line_items": []
    }

    if result.document and result.document.inference.prediction:
        prediction = result.document.inference.prediction
        if prediction.supplier_name:
            extracted_data["merchant_name"] = prediction.supplier_name.value
        if prediction.total_amount:
            extracted_data["total_amount"] = prediction.total_amount.value
        if prediction.total_tax:
            extracted_data["tax_amount"] = prediction.total_tax.value
        
        for item in prediction.line_items:
            extracted_data["line_items"].append({
                "description": item.description,
                "quantity": item.quantity,
                "price": item.price_unit,
                "total": item.total_amount
            })

    return extracted_data

if __name__ == "__main__":
    # Example usage (replace with your actual API key and file path)
    MINDEE_API_KEY = os.environ.get("MINDEE_API_KEY", "YOUR_MINDEE_API_KEY")
    FILE_PATH = "path/to/your/receipt.jpg"

    # result = extract_receipt_fields(MINDEE_API_KEY, FILE_PATH)
    # print(result)
