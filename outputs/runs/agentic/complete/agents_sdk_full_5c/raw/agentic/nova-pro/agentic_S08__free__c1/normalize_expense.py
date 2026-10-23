import boto3

def normalize_expense(expense_data):
    # Normalization logic here
    return {'vendor': expense_data['vendor'], 'date': expense_data['date'], 'amount': expense_data['total']}