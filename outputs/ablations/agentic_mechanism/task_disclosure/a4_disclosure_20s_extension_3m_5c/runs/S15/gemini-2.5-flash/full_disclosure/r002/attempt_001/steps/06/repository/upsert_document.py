import boto3
import os
import json

def upsert_document(table_name: str, document: dict, primary_key_name: str):
    """
    Upserts a JSON document into an AWS DynamoDB table.

    Args:
        table_name (str): The name of the DynamoDB table.
        document (dict): The JSON document to upsert. It must contain the primary key.
        primary_key_name (str): The name of the primary key attribute in the document.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Ensure the document contains the primary key
    if primary_key_name not in document:
        raise ValueError(f"Document must contain the primary key '{primary_key_name}'")

    response = table.put_item(
        Item=document
    )
    return response
