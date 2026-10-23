import os
import boto3
from document_client import DocumentAIClient
from document_models import ReceiptFields, LineItem, ExtractionResult

def extract_receipt_fields(file_path: str) -> ExtractionResult:
    textract_client = DocumentAIClient().get_textract_client()

    with open(file_path, 'rb') as document:
        image_bytes = bytearray(document.read())

    try:
        response = textract_client.analyze_expense(Document={'Bytes': image_bytes})

        receipt_fields = ReceiptFields()
        total_confidence = 0.0
        field_count = 0

        for expense_document in response['ExpenseDocuments']:
            for line_item_group in expense_document['LineItemGroups']:
                for line_item in line_item_group['LineItems']:
                    for expense_field in line_item['LineItemExpenseFields']:
                        if expense_field['Type']['Text'] == 'ITEM_DESCRIPTION' and 'ValueDetection' in expense_field:
                            description = expense_field['ValueDetection']['Text']
                        elif expense_field['Type']['Text'] == 'PRICE' and 'ValueDetection' in expense_field:
                            total = float(expense_field['ValueDetection']['Text'])
                            receipt_fields.line_items.append(LineItem(description=description, total=total))

            for field in expense_document['SummaryFields']:
                field_type = field['Type']['Text']
                if 'ValueDetection' in field:
                    value = field['ValueDetection']['Text']
                    confidence = field['ValueDetection']['Confidence']
                    total_confidence += confidence
                    field_count += 1

                    if field_type == 'MERCHANT_NAME':
                        receipt_fields.merchant_name = value
                    elif field_type == 'DATE':
                        receipt_fields.transaction_date = value
                    elif field_type == 'TOTAL':
                        receipt_fields.total_amount = float(value)
                        if 'Currency' in field:
                            receipt_fields.currency = field['Currency']['Text']
                    elif field_type == 'TAX':
                        receipt_fields.tax_amount = float(value)

        avg_confidence = total_confidence / field_count if field_count > 0 else 0.0

        return ExtractionResult(
            success=True,
            data=receipt_fields.to_dict(),
            confidence=avg_confidence
        )
    except Exception as e:
        return ExtractionResult(
            success=False,
            error=str(e)
        )
