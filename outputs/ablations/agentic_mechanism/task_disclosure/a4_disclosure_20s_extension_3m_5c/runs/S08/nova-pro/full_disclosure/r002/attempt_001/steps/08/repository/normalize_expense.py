import boto3

def normalize_expense_fields(expense_fields):
    # Create a Lambda client
    lambda_client = boto3.client('lambda')
    
    # Define the payload
    payload = {
        'expense_fields': expense_fields
    }
    
    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName='normalize-expense',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    # Get the response payload
    normalized_fields = json.loads(response['Payload'].read())
    
    return normalized_fields