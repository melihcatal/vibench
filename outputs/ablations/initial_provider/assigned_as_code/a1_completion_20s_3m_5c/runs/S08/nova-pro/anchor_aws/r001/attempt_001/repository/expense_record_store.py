import boto3

def store_expense_record(expense_record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='ExpenseRecords',
        Item={
            'Vendor': {'S': expense_record['vendor']},
            'Date': {'S': expense_record['date']},
            'Total': {'N': expense_record['total']},
            'Items': {'L': [{'M': {'Description': {'S': item['description']}, 'Quantity': {'N': item['quantity']}, 'Amount': {'N': item['amount']}}} for item in expense_record['items']]}
        }
    )