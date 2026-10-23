import json


def normalize_expense(expense_fields):
    normalized_expense = {}
    normalized_expense["vendor"] = expense_fields.get("vendor")
    normalized_expense["date"] = expense_fields.get("date")
    normalized_expense["total"] = expense_fields.get("total")
    normalized_expense["line_items"] = expense_fields.get("line_items")
    return json.dumps(normalized_expense, indent=2)
