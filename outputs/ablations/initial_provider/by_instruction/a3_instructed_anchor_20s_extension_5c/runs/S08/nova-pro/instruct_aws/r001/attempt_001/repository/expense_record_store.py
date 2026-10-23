import boto3

def store_expense_record(expense):
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_client.put_item(
        TableName='ExpenseRecords',
        Item={
            'Vendor': {'S': expense['vendor']},
            'Date': {'S': expense['date']},
            'Total': {'N': expense['total']},
            'LineItems': {'L': [{'S': item} for item in expense['line_items']]}
        }
    )