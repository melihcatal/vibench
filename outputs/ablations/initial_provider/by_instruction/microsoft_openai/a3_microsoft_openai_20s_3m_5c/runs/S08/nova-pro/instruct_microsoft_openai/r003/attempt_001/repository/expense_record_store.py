import boto3

def store_expense_record(expense: Dict[str, Any]):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ExpenseRecords')
    table.put_item(Item=expense)