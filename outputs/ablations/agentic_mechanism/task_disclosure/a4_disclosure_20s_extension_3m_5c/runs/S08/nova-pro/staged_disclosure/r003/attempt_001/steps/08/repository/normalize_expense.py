import boto3

def normalize_expense(expense_data):
    comprehend = boto3.client('comprehend')
    
    # Example normalization using Amazon Comprehend
    # This is a placeholder for actual normalization logic
    normalized_data = comprehend.detect_sentiment(
        Text=expense_data['description'],
        LanguageCode='en'
    )
    
    # Return normalized data in a standard JSON schema
    return {
        'description': expense_data['description'],
        'sentiment': normalized_data['Sentiment']
    }

if __name__ == '__main__':\n    sample_expense = {'description': 'Dinner with client'}\n    print(normalize_expense(sample_expense))