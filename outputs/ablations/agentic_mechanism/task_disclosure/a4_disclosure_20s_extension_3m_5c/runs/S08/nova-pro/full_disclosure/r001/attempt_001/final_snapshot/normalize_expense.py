import boto3

def normalize_expense(expense_data):
    # Configure the AWS Lambda client
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Invoke the AWS Lambda function to normalize the expense data
    response = lambda_client.invoke(
        FunctionName='expense-normalization-function',
        InvocationType='RequestResponse',
        Payload=json.dumps(expense_data)
    )
    
    # Read the response from the Lambda function
    payload = json.loads(response['Payload'].read())
    
    return payload