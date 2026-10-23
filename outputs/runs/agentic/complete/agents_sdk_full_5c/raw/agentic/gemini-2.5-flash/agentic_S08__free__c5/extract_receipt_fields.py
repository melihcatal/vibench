import os
import boto3

def extract_receipt_fields(file_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract.
    """
    textract_client = boto3.client('textract', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    with open(file_path, 'rb') as document:
        image_bytes = bytearray(document.read())

    response = textract_client.analyze_expense(Document={'Bytes': image_bytes})

    extracted_data = {
        "merchant_name": "",
        "tax_amount": "",
        "total_amount": "",
        "line_items": []
    }

    for expense_document in response['ExpenseDocuments']:
        for field in expense_document['SummaryFields']:
            if field['Type']['Text'] == 'VENDOR_NAME' and 'ValueDetection' in field:
                extracted_data["merchant_name"] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TAX' and 'ValueDetection' in field:
                extracted_data["tax_amount"] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TOTAL' and 'ValueDetection' in field:
                extracted_data["total_amount"] = field['ValueDetection']['Text']
        
        for line_item_group in expense_document['LineItemGroups']:
            for line_item in line_item_group['LineItems']:
                item = {}
                for field in line_item['LineItemFields']:
                    if field['Type']['Text'] == 'ITEM' and 'ValueDetection' in field:
                        item['description'] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'QUANTITY' and 'ValueDetection' in field:
                        item['quantity'] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'PRICE' and 'ValueDetection' in field:
                        item['unit_price'] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'TOTAL' and 'ValueDetection' in field:
                        item['amount'] = field['ValueDetection']['Text']
                if item:
                    extracted_data["line_items"].append(item)

    return extracted_data

if __name__ == '__main__':
    # This is a placeholder for actual credential/config loading
    # Make sure to have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)
    # and AWS_REGION set.
    try:
        # Example usage - replace with a real image file (e.g., JPG, PNG, PDF)
        # result = extract_receipt_fields("path/to/your/receipt.png")
        # print("Extracted Receipt Fields:", result)
        print("To run, provide an image file path and ensure AWS credentials and region are configured.")
    except Exception as e:
        print(f"Error extracting receipt fields: {e}")

