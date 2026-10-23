from document_models import normalize_expense_record


def normalize_expense(payload, config=None):
    expense = payload.get('expense') or payload.get('record') or {}
    normalized = normalize_expense_record(expense)
    normalized['source'] = 'azure-ai-documentintelligence'
    return {'normalized_expense': normalized}
