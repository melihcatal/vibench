import os
import boto3

def extract_receipt_fields(file_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    client = boto3.client('textract',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                          region_name=os.environ.get("AWS_REGION_NAME"))

    with open(file_path, "rb") as document:
        response = client.analyze_expense(Document={'Bytes': document.read()})

    extracted_data = {}
    if response.get('ExpenseDocuments'):
        expense_doc = response['ExpenseDocuments'][0]
        # Extract summary fields
        for field in expense_doc.get('SummaryFields', []):
            if field['Type']['Text'] == 'MERCHANT_NAME':
                extracted_data['merchant_name'] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TOTAL':
                extracted_data['total'] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TAX':
                extracted_data['tax'] = field['ValueDetection']['Text']
        
        # Extract line items (simplified)
        line_items = []
        for line_item_group in expense_doc.get('LineItemGroups', []):
            for item in line_item_group.get('LineItems', []):
                item_data = {}
                for field in item.get('LineItemExpenseFields', []):
                    if field['Type']['Text'] == 'ITEM':
                        item_data['description'] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'PRICE':
                        item_data['amount'] = field['ValueDetection']['Text']
                    # Add other fields like quantity if needed
                if item_data: # Only add if some data was extracted
                    line_items.append(item_data)
        extracted_data['line_items'] = line_items

    return extracted_data

if __name__ == '__main__':
    RECEIPT_FILE = "path/to/your/receipt.png" # Replace with actual path
    # Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME environment variables

    if not os.path.exists(RECEIPT_FILE):
        print(f"Dummy file not found at {RECEIPT_FILE}. Skipping extraction demo.")
        print("Please create a dummy receipt.png or provide a real one to run this example.")
    else:
        print(f"Extracting fields from {RECEIPT_FILE}...")
        fields = extract_receipt_fields(RECEIPT_FILE)
        print("Extracted Receipt Fields:", fields)
