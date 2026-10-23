import boto3

def normalize_expense(expense_fields):
    comprehend = boto3.client('comprehend')
    normalized_expense = {}
    for field, value in expense_fields.items():
        if field == 'vendor':
            normalized_expense['vendor'] = comprehend.detect_entities(Text=value, LanguageCode='en')
        elif field == 'date':
            normalized_expense['date'] = comprehend.detect_syntax(Text=value, LanguageCode='en')
        elif field == 'total':
            normalized_expense['total'] = comprehend.detect_key_phrases(Text=value, LanguageCode='en')
        else:
            normalized_expense[field] = value
    return normalized_expense