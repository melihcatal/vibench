from typing import List
from document_models import ExpenseRecord


def validate_document_fields(expense_record: ExpenseRecord) -> List[str]:
    errors = []
    if expense_record.document_type == "invoice":
        if not expense_record.vendor_name:
            errors.append("Invoice must have a vendor name.")
        if not expense_record.transaction_date:
            errors.append("Invoice must have a transaction date.")
        if not expense_record.total_amount:
            errors.append("Invoice must have a total amount.")
    elif expense_record.document_type == "receipt":
        if not expense_record.merchant_name:
            errors.append("Receipt must have a merchant name.")
        if not expense_record.total_amount:
            errors.append("Receipt must have a total amount.")
    
    # Example of confidence score validation (if scores were available in ExpenseRecord)
    # if expense_record.total_amount_confidence and expense_record.total_amount_confidence < 0.7:
    #     errors.append("Total amount confidence is too low.")

    return errors
