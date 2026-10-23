import boto3

def normalize_expense(expense_data):
    comprehend = boto3.client('comprehend')
    normalized_data = {}
    
    # Example normalization using Amazon Comprehend
    if 'description' in expense_data:
        description = expense_data['description']
        response = comprehend.detect_entities(Text=description, LanguageCode='en')
        normalized_data['entities'] = response['Entities']
    
    return normalized_data
