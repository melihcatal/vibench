import os
import boto3
from document_client import get_textract_client
from document_models import NormalizedExpense, LineItem

def extract_receipt_fields(file_path: str) -> NormalizedExpense:
    """
    Extracts receipt fields using Amazon Textract's AnalyzeExpense API.
    """
    client = get_textract_client()

    with open(file_path, 'rb') as document:
        image_bytes = bytearray(document.read())

    response = client.analyze_expense(Document={'Bytes': image_bytes})

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    line_items = []

    merchant_name_confidence = 0.0
    transaction_date_confidence = 0.0
    total_amount_confidence = 0.0
    tax_amount_confidence = 0.0

    for expense_document in response['ExpenseDocuments']:
        for field in expense_document['SummaryFields']:
            if field['Type']['Text'] == 'MERCHANT_NAME':
                merchant_name = field['ValueDetection']['Text']
                merchant_name_confidence = field['ValueDetection']['Confidence'] / 100.0
            elif field['Type']['Text'] == 'DATE':
                transaction_date = field['ValueDetection']['Text']
                transaction_date_confidence = field['ValueDetection']['Confidence'] / 100.0
            elif field['Type']['Text'] == 'TOTAL':
                total_amount = float(field['ValueDetection']['Text']) if field['ValueDetection']['Text'] else None
                currency = field['CurrencyDetection']['Text'] if 'CurrencyDetection' in field else None
                total_amount_confidence = field['ValueDetection']['Confidence'] / 100.0
            elif field['Type']['Text'] == 'TAX':
                tax_amount = float(field['ValueDetection']['Text']) if field['ValueDetection']['Text'] else None
                tax_amount_confidence = field['ValueDetection']['Confidence'] / 100.0

        for line_item_group in expense_document['LineItemGroups']:
            for item in line_item_group['LineItems']:
                item_description = None
                item_quantity = None
                item_unit_price = None
                item_total_price = None
                for field in item['LineItemExpenseFields']:
                    if field['Type']['Text'] == 'ITEM':
                        item_description = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'QUANTITY':
                        item_quantity = float(field['ValueDetection']['Text']) if field['ValueDetection']['Text'] else None
                    elif field['Type']['Text'] == 'PRICE': # Often unit price
                        item_unit_price = float(field['ValueDetection']['Text']) if field['ValueDetection']['Text'] else None
                    elif field['Type']['Text'] == 'TOTAL': # Often line item total
                        item_total_price = float(field['ValueDetection']['Text']) if field['ValueDetection']['Text'] else None
                line_items.append(LineItem(description=item_description, quantity=item_quantity,
                                           unit_price=item_unit_price, total_price=item_total_price))

    confidence_scores = {
        "merchant_name": merchant_name_confidence,
        "transaction_date": transaction_date_confidence,
        "total_amount": total_amount_confidence,
        "tax_amount": tax_amount_confidence,
    }

    return NormalizedExpense(
        document_type="receipt",
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        raw_text=response['DocumentMetadata']['TextractFeatures'][0] if 'TextractFeatures' in response['DocumentMetadata'] else None, # Not really raw text but just to fill the field
        confidence_scores=confidence_scores
    )

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with your actual file path.
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as environment variables.
    # file_path = "path/to/your/receipt.pdf"
    #
    # if os.path.exists(file_path):
    #     extracted_data = extract_receipt_fields(file_path)
    #     print(extracted_data.json(indent=2))
    # else:
    #     print("Please set AWS environment variables and provide a valid file_path.")
    pass
