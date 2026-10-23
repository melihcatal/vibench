import os
import boto3
from botocore.exceptions import ClientError

def conditional_update_document(
    table_name: str,
    key: dict,
    update_expression: str,
    expression_attribute_values: dict,
    condition_expression: str,
    expression_attribute_names: dict | None = None
):
    """
    Applies a conditional update to a document in DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        key (dict): A dictionary representing the primary key of the item.
        update_expression (str): The expression for the update operation.
        expression_attribute_values (dict): A dictionary of values for the expression.
        condition_expression (str): The condition that must be met for the update to succeed.
        expression_attribute_names (dict, optional): A dictionary of attribute name mappings.
                                                    Defaults to None.
    """
    # AWS DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    try:
        update_args = {
            'TableName': table_name,
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ConditionExpression': condition_expression,
            'ReturnValues': "UPDATED_NEW"
        }
        if expression_attribute_names:
            update_args['ExpressionAttributeNames'] = expression_attribute_names

        response = dynamodb.update_item(**update_args)
        print(f"Conditional update successful: {response}")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Conditional check failed: The item was not updated because the condition was not met.")
        else:
            print(f"Error updating item: {e}")
        return None

if __name__ == "__main__":
    # AWS_REGION environment variable should be set, e.g., 'us-east-1'
    # AWS credentials should be configured, e.g., via AWS CLI or environment variables.

    # Replace with your DynamoDB table name.
    # A table named "MyConditionalUpdateTable" with a primary key 'id' (String) is assumed.
    TABLE_NAME = "MyConditionalUpdateTable"

    dynamodb_client = boto3.client('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    # 1. Put an initial item
    item_id = 'doc123'
    initial_version = 1
    initial_data = 'initial data'

    try:
        dynamodb_client.put_item(
            TableName=TABLE_NAME,
            Item={
                'id': {'S': item_id},
                'version': {'N': str(initial_version)},
                'data': {'S': initial_data}
            }
        )
        print(f"Initial item '{item_id}' with version {initial_version} put successfully.")
    except ClientError as e:
        print(f"Error putting initial item: {e}")

    # 2. Attempt a conditional update (will succeed if version is 1)
    print(f"\nAttempting conditional update for '{item_id}' with expected version {initial_version}...")
    new_data_value = 'updated data v2'
    expected_version_for_update_1 = initial_version
    new_version_1 = initial_version + 1

    conditional_update_document(
        table_name=TABLE_NAME,
        key={'id': {'S': item_id}},
        update_expression="SET #data = :newData, #version = :newVersion",
        expression_attribute_values={
            ":newData": {'S': new_data_value},
            ":newVersion": {'N': str(new_version_1)},
            ":expectedVersion": {'N': str(expected_version_for_update_1)}
        },
        condition_expression="#version = :expectedVersion",
        expression_attribute_names={
            "#version": "version",
            "#data": "data"
        }
    )

    # 3. Attempt another conditional update (will fail because expected version is now incorrect)
    print(f"\nAttempting conditional update for '{item_id}' with expected version {expected_version_for_update_1} again (expected to fail)...")
    new_data_value_fail = 'data that should not be written'
    expected_version_for_update_2 = expected_version_for_update_1
    new_version_2 = new_version_1 + 1

    conditional_update_document(
        table_name=TABLE_NAME,
        key={'id': {'S': item_id}},
        update_expression="SET #data = :newData, #version = :newVersion",
        expression_attribute_values={
            ":newData": {'S': new_data_value_fail},
            ":newVersion": {'N': str(new_version_2)},
            ":expectedVersion": {'N': str(expected_version_for_update_2)}
        },
        condition_expression="#version = :expectedVersion",
        expression_attribute_names={
            "#version": "version",
            "#data": "data"
        }
    )

    # 4. Attempt a conditional update that should succeed with the current version (2)
    print(f"\nAttempting conditional update for '{item_id}' with expected version {new_version_1} (expected to succeed)...")
    new_data_value_success = 'final updated data v3'
    expected_version_for_update_3 = new_version_1
    new_version_3 = new_version_1 + 1

    conditional_update_document(
        table_name=TABLE_NAME,
        key={'id': {'S': item_id}},
        update_expression="SET #data = :newData, #version = :newVersion",
        expression_attribute_values={
            ":newData": {'S': new_data_value_success},
            ":newVersion": {'N': str(new_version_3)},
            ":expectedVersion": {'N': str(expected_version_for_update_3)}
        },
        condition_expression="#version = :expectedVersion",
        expression_attribute_names={
            "#version": "version",
            "#data": "data"
        }
    )

    # 5. Read the item to verify
    print(f"\nReading the final item '{item_id}' to verify...")
    try:
        response = dynamodb_client.get_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': item_id}}
        )
        print(f"Final item: {response.get('Item')}")
    except ClientError as e:
        print(f"Error reading item: {e}")