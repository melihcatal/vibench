import json


def summarize_invoice(expense):
    summary = {
        "vendor": expense.get("vendor_or_merchant", "N/A"),
        "date": expense.get("date", "N/A"),
        "total": expense.get("total", "N/A"),
        "line_item_count": len(expense.get("line_items", [])),
        "tax": expense.get("tax", "N/A"),
    }
    return summary
