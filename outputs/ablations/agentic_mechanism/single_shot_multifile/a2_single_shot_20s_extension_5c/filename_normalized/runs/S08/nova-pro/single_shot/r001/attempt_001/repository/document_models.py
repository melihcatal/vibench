def normalize_expense_fields(expense):
    normalized_expense = {}
    for field, value in expense.items():
        normalized_expense[field.lower()] = value
    return normalized_expense

def validate_expense_fields(expense):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in expense or not expense[field]:
            return False, f'{field} is missing or empty'
    return True, 'All required fields are present'