import boto3

def store_expense_record(expense):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ExpenseRecords')
    response = table.put_item(Item=expense)
    return response

if __name__ == '__main__':
    expense = {
        'ExpenseID': '1',
        'Amount': 100.0,
        'Date': '2026-09-20',
        'Category': 'Travel'
    }
    response = store_expense_record(expense)
    print(response)