
import boto3
import os

def extract_receipt_fields(file_bytes: bytes) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract.
    """
    textract_client = boto3.client('textract', region_name=os.getenv("AWS_REGION", "us-east-1"))

    response = textract_client.analyze_expense(
        Document={'Bytes': file_bytes}
    )

    extracted_data = {
        "merchant_name": "",
        "tax_amount": "",
        "total_amount": "",
        "items": []
    }

    if response.get("ExpenseDocuments"):
        expense_document = response["ExpenseDocuments"][0]

        # Extract summary fields
        for field in expense_document.get("SummaryFields", []):
            if field.get("Type", {}).get("Text") == "VENDOR_NAME":
                extracted_data["merchant_name"] = field.get("ValueDetection", {}).get("Text", "")
            elif field.get("Type", {}).get("Text") == "TOTAL_TAX":
                extracted_data["tax_amount"] = field.get("ValueDetection", {}).get("Text", "")
            elif field.get("Type", {}).get("Text") == "TOTAL":
                extracted_data["total_amount"] = field.get("ValueDetection", {}).get("Text", "")

        # Extract line items
        for line_item_group in expense_document.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item_data = {}
                for field in line_item.get("LineItemFields", []):
                    field_type = field.get("Type", {}).get("Text")
                    field_value = field.get("ValueDetection", {}).get("Text", "")
                    if field_type == "ITEM":
                        item_data["description"] = field_value
                    elif field_type == "PRICE":
                        item_data["amount"] = field_value
                    elif field_type == "QUANTITY":
                        item_data["quantity"] = field_value
                if item_data:
                    extracted_data["items"].append(item_data)

    return extracted_data

if __name__ == '__main__':
    # Example usage placeholder:
    # RECIEPT_PATH = "path/to/your/receipt.jpg"
    # if os.path.exists(RECIEPT_PATH):
    #     with open(RECIEPT_PATH, "rb") as image_file:
    #         receipt_bytes = image_file.read()
    #     extracted_receipt_data = extract_receipt_fields(receipt_bytes)
    #     print("Extracted Receipt Data:", extracted_receipt_data)
    # else:
    #     print("Please provide a valid path to a receipt image.")
    pass
