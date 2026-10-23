import boto3

def store_expense_record(expense):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName='ExpenseRecords',
        Item={
            'ExpenseId': {'S': str(uuid.uuid4())},
            'Vendor': {'S': expense['vendor']},
            'Date': {'S': expense['date']},
            'Total': {'N': str(expense['total'])},
            'LineItems': {'S': json.dumps(expense['line_items'])},
            'Merchant': {'S': expense['merchant']},
            'Tax': {'N': str(expense['tax'])},
            'Items': {'S': json.dumps(expense['items'])}
        }
    )
