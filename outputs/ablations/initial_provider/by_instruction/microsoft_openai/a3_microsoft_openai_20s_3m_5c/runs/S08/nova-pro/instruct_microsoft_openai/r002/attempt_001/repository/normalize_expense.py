from document_models import Expense

def normalize_expense(expense_fields):
    expense = Expense(
        vendor=expense_fields.get("vendor"),
        date=expense_fields.get("date"),
        total=expense_fields.get("total"),
        items=expense_fields.get("line_items", [])
    )
    return expense.to_json()