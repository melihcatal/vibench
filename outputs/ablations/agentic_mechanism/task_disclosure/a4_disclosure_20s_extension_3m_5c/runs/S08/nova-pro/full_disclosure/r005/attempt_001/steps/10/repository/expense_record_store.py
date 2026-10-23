import boto3

dynamodb = boto3.resource('dynamodb')

def store_expense_record(table_name, record):
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)

if __name__ == '__main__':
    # Example usage
    expense_record = {
        'id': '1',
        'vendor': 'Example Vendor',
        'date': '2026-09-20',
        'total': 100.00,
        'items': [
            {'description': 'Item 1', 'amount': 50.00},
            {'description': 'Item 2', 'amount': 50.00}
        ]
    }
    store_expense_record('ExpenseRecords', expense_record)