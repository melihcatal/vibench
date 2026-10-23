# Provider: UiPath Document Understanding (Document Extraction)
# Provider identifier present via import above

import json
from document_models import ExpenseRecord


def normalize_expense(raw_response: dict) -> ExpenseRecord:
    """Normalize extracted fields into a standard JSON schema (ExpenseRecord).
    Converts vendor/date/total/line_items (invoice) or merchant/tax/total/items (receipt) into a unified model.
    """
    # Determine source type based on keys present
    if "vendor" in raw_response:
        expense = ExpenseRecord(
            vendor=raw_response["vendor"],
            date=raw_response.get("date"),
            total=raw_response.get("total"),
            line_items=raw_response.get("line_items", []),
        )
    elif "merchant" in raw_response:
        expense = ExpenseRecord(
            merchant=raw_response["merchant"],
            tax=raw_response.get("tax"),
            total=raw_response.get("total"),
            items=raw_response.get("items", []),
        )
    else:
        raise ValueError("Unsupported document type for normalization")
    return expense
