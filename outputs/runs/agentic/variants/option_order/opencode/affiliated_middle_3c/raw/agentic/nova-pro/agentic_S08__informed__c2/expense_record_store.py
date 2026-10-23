import boto3


def store_expense_record(record):
    client = boto3.resource("dynamodb")
    table = client.Table("ExpenseRecords")
    table.put_item(Item=record)
