from.document_models import NormalizedExpense

def validate_document_fields(expense: NormalizedExpense):
    if not expense.vendor or not expense.date or not expense.total:
        raise ValueError('Missing required fields')
    if expense.total <= 0:
        raise ValueError('Total must be greater than zero')