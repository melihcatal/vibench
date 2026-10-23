import os
import boto3
from botocore.exceptions import ClientError

def upsert_document(table_name: str, document: dict, region_name: str = None):
    """
    Upserts a JSON document into an AWS DynamoDB table.

    Args:
        table_name (str): The name of the DynamoDB table.
        document (dict): The JSON document to upsert. This dictionary must
                         include the primary key attribute(s) of the table.
        region_name (str, optional): The AWS region to connect to. If not provided,
                                     it will use the AWS_REGION environment variable
                                     or the default region configured in boto3.

    Returns:
        dict: The response from the DynamoDB put_item operation.
        None: If an error occurs.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1") # Defaulting to us-east-1 for identifiability if not set

    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=document)
        return response
    except ClientError as e:
        print(f"Error upserting document: {e.response['Error']['Message']}")
        return None
