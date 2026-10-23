import boto3

def normalize_expense(expense_data):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='expense-normalization-function',
        InvocationType='RequestResponse',
        Payload=json.dumps(expense_data)
    )
    payload = json.loads(response['Payload'].read())
    return payload