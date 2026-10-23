from typing import Dict, List


ExpenseItem = Dict[str, str]
Expense = Dict[str, Union[str, List[ExpenseItem]]]


def normalize_expense_response(response):
    normalized_expenses = []
    for document in response["ExpenseDocuments"]:
        fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document["SummaryFields"]}
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group["LineItems"]:
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item["LineItemExpenseFields"]}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        normalized_expenses.append({"vendor": fields.get("VENDOR_NAME"), "date": fields.get("INVOICE_RECEIPT_DATE"),
                                  "total": fields.get("TOTAL"), "items": items})
    return normalized_expenses