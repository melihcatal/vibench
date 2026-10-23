import boto3

# Initialize a session using Amazon DynamoDB
session = boto3.Session()

# Initialize the DynamoDB client
dynamodb = session.client('dynamodb')

# Define the table name
table_name = 'ExampleTable'

# Define the key for the item to update
key = {'Id': {'N': '1'}}

# Define the update expression
update_expression = 'SET info.title = :val1'

# Define the expression attribute values
expression_attribute_values = {':val1': {'S': 'New Title'}}

# Define the condition expression
condition_expression = 'attribute_exists(info.title)'

# Perform the conditional update
response = dynamodb.update_item(
    TableName=table_name,
    Key=key,
    UpdateExpression=update_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ConditionExpression=condition_expression
)

print(response)