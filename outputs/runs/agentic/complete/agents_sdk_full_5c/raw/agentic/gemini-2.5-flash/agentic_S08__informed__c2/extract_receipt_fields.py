import os
import boto3
from document_models import ReceiptExtractionResult, LineItem

def extract_receipt_fields(file_content: bytes) -> ReceiptExtractionResult:
    textract_client = boto3.client('textract', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = textract_client.analyze_expense(Document={'Bytes': file_content})

    merchant_name = ""
    tax_amount = 0.0
    total_amount = 0.0
    items = []

    for doc_group in response.get("ExpenseDocuments", []):
        for field in doc_group.get("SummaryFields", []):
            if field.get("Type", {}).get("Text") == "VENDOR_NAME":
                merchant_name = field.get("ValueDetection", {}).get("Text", "")
            elif field.get("Type", {}).get("Text") == "TOTAL":
                try:
                    total_amount = float(field.get("ValueDetection", {}).get("Text", "").replace("$", "").replace(",", ""))
                except ValueError:
                    pass
            elif field.get("Type", {}).get("Text") == "TAX":
                try:
                    tax_amount = float(field.get("ValueDetection", {}).get("Text", "").replace("$", "").replace(",", ""))
                except ValueError:
                    pass

        for line_item_group in doc_group.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item_description = ""
                item_amount = 0.0
                for field in line_item.get("LineItemExpenseFields", []):
                    if field.get("Type", {}).get("Text") == "ITEM":
                        item_description = field.get("ValueDetection", {}).get("Text", "")
                    elif field.get("Type", {}).get("Text") == "PRICE":
                        try:
                            item_amount = float(field.get("ValueDetection", {}).get("Text", "").replace("$", "").replace(",", ""))
                        except ValueError:
                            pass
                if item_description or item_amount:
                    items.append(LineItem(description=item_description, amount=item_amount))

    return ReceiptExtractionResult(
        merchant=merchant_name,
        tax=tax_amount,
        total=total_amount,
        items=items
    )

if __name__ == '__main__':
    # Example usage:
    # with open("receipt.pdf", "rb") as f:
    #     content = f.read()
    # result = extract_receipt_fields(content)
    # print(result)
    pass
