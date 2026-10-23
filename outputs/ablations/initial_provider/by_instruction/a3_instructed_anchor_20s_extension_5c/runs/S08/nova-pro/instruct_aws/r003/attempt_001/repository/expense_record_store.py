import boto3

def store_expense_record(expense_record):
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_client.put_item(
        TableName='ExpenseRecords',
        Item={
            'Vendor': {'S': expense_record['vendor']},
            'Date': {'S': expense_record['date']},
            'Total': {'N': expense_record['total']},
            'Items': {'L': [{'S': item} for item in expense_record['items']]}
        }
    )