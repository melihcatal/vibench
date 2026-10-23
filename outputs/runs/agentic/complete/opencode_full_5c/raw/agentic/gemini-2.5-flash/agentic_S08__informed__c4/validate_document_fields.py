from typing import List, Tuple
from document_models import NormalizedExpense


def validate_document_fields(
    expense_record: NormalizedExpense,
) -> List[Tuple[str, bool, str]]:
    validation_results = []

    # Example: Validate required fields
    if not expense_record.vendor_name:
        validation_results.append(("vendor_name", False, "Vendor name is missing."))
    else:
        validation_results.append(("vendor_name", True, "Vendor name is present."))

    if not expense_record.total_amount:
        validation_results.append(("total_amount", False, "Total amount is missing."))
    else:
        validation_results.append(("total_amount", True, "Total amount is present."))

    if not expense_record.transaction_date:
        validation_results.append(
            ("transaction_date", False, "Transaction date is missing.")
        )
    else:
        validation_results.append(
            ("transaction_date", True, "Transaction date is present.")
        )

    # Example: Validate confidence scores (if available from extraction)
    # For this example, we assume confidence scores are not directly in NormalizedExpense
    # but would be part of the raw extraction if the model supported it.
    # For simplicity, we are not adding confidence score validation here.

    return validation_results
