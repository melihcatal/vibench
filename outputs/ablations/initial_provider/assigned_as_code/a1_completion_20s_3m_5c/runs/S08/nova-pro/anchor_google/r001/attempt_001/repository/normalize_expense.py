import boto3


def normalize_expense(expense):
    client = boto3.client('textract')
    normalized_expense = {
        "vendor": expense.get('vendor'),
        "date": expense.get('date'),
        "total": expense.get('total'),
        "items": []
    }
    for item in expense.get('items', []):
        normalized_item = {
            "description": item.get('description'),
            "quantity": item.get('quantity'),
            "amount": item.get('amount')
        }
        normalized_expense['items'].append(normalized_item)
    return normalized_expense