import json
from normalize_expense import NormalizeExpense
from validate_document_fields import ValidateDocumentFields


class InvoiceSummary:
    @staticmethod
    def summarize(normalized_expense: NormalizeExpense):
        # Generate a concise summary of the invoice
        summary = {
            "vendor": normalized_expense.vendor,
            "date": normalized_expense.date,
            "total": normalized_expense.total,
            "line_items_count": len(normalized_expense.line_items),
        }
        return json.dumps(summary, indent=2)
