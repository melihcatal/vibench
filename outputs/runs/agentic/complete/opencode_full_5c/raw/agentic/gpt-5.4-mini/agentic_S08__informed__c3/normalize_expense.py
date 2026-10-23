from document_models import NormalizedExpense, normalize_expense_payload

def normalize_expense(request):
    payload = normalize_expense_payload(request)
    return NormalizedExpense.from_payload(payload).to_dict()
