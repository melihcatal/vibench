import boto3

def normalize_expense(expense_data):
    comprehend = boto3.client('comprehend')
    normalized_expense = {}
    for field, value in expense_data.items():
        if field == 'description':
            response = comprehend.detect_entities(Text=value, LanguageCode='en')
            normalized_expense[field] = response['Entities']
        else:
            normalized_expense[field] = value
    return normalized_expense