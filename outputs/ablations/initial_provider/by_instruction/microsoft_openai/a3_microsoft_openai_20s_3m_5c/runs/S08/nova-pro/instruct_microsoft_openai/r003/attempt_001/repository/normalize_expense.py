from.document_models import NormalizedExpense

def normalize_expense(expense: NormalizedExpense):
    return {
        'vendor': expense.vendor,
        'date': expense.date,
        'total': expense.total,
        'items': expense.items
    }