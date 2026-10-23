import os
import json
from typing import Dict, Any, Optional
from database_client import get_dynamodb_client
from database_models import DocumentUpdate
import botocore.exceptions

def conditional_update(table_name: str, document_id: str, update_payload: DocumentUpdate) -> Dict[str, Any]:
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    Assumes a 'version' attribute for optimistic locking.
    
    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary identifier of the document to update.
        update_payload: An DocumentUpdate object containing updates and an optional version for optimistic locking.
        
    Returns:
        The response from the DynamoDB update_item operation.
        
    Raises:
        ValueError: If the document version does not match or the update fails due to a condition.
    """
    dynamodb = get_dynamodb_client()
    
    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    
    # Increment version automatically if not explicitly provided in updates
    # And ensure the existing version matches if provided in payload
    if update_payload.version is not None:
        # Condition for optimistic locking
        condition_expression = f"#version = :current_version"
        expression_attribute_names["#version"] = "version"
        expression_attribute_values[":current_version"] = {"N": str(update_payload.version)}
    else:
        condition_expression = None # No version-aware condition by default

    # Build UpdateExpression and ExpressionAttributeValues for content updates
    for key, value in update_payload.updates.items():
        if key == "version": # Handle version separately or ignore if already handled
            continue
        
        update_expression_parts.append(f"#{key} = :{key}")
        expression_attribute_names[f"#{key}"] = key
        
        if isinstance(value, str):
            expression_attribute_values[f":{key}"] = {"S": value}
        elif isinstance(value, (int, float)):
            expression_attribute_values[f":{key}"] = {"N": str(value)}
        elif isinstance(value, bool):
            expression_attribute_values[f":{key}"] = {"BOOL": value}
        else:
            expression_attribute_values[f":{key}"] = {"S": str(value)} # Fallback
            
    # Always increment the version in the update expression
    if "#version" not in expression_attribute_names:
         expression_attribute_names["#version"] = "version"
    update_expression_parts.append("#version = #version + :inc")
    expression_attribute_values[":inc"] = {"N": "1"}

    update_expression = "SET " + ", ".join(update_expression_parts)
    
    try:
        update_args = {
            "TableName": table_name,
            "Key": {'id': {'S': document_id}},
            "UpdateExpression": update_expression,
            "ExpressionAttributeNames": expression_attribute_names,
            "ExpressionAttributeValues": expression_attribute_values,
            "ReturnValues": "ALL_NEW"
        }
        if condition_expression:
            update_args["ConditionExpression"] = condition_expression
            
        response = dynamodb.update_item(**update_args)
        return response
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Conditional update failed: Document with ID '{document_id}' version mismatch or condition not met.") from e
        else:
            raise # Re-raise other exceptions

if __name__ == "__main__":
    # Example Usage (requires AWS credentials and DynamoDB table configured)
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "your-document-table")
    target_id = "doc123"
    
    # First, let's upsert a document with a version to ensure it exists
    from upsert_document import upsert_document
    sample_doc_initial = Document(
        id=target_id,
        data={
            "title": "Original Title",
            "author": "Jane Doe",
            "version": 1
        }
    )
    try:
        upsert_document(table_name, sample_doc_initial)
        print(f"Initial document {target_id} upserted.")
    except Exception as e:
        print(f"Error during initial upsert: {e}")

    # Scenario 1: Successful conditional update with correct version
    print(f"\nAttempting successful conditional update for {target_id}...")
    update_payload_success = DocumentUpdate(
        updates={
            "title": "Updated Title V2",
            "status": "published"
        },
        version=1 # Expecting current version to be 1
    )
    try:
        response = conditional_update(table_name, target_id, update_payload_success)
        print("Successful update response:", json.dumps(response, indent=2))
    except ValueError as e:
        print(f"Caught expected error for successful update: {e}")
    except Exception as e:
        print(f"Unexpected error during successful update: {e}")

    # Scenario 2: Failed conditional update with incorrect version
    print(f"\nAttempting failed conditional update for {target_id} (incorrect version)...")
    update_payload_fail = DocumentUpdate(
        updates={
            "title": "Attempted Update V3",
        },
        version=1 # Still expecting current version to be 1, but it's now 2
    )
    try:
        response = conditional_update(table_name, target_id, update_payload_fail)
        print("Failed update response (unexpected success):", json.dumps(response, indent=2))
    except ValueError as e:
        print(f"Caught expected error for failed update: {e}")
    except Exception as e:
        print(f"Unexpected error during failed update: {e}")

    # Scenario 3: Update without explicit version, still increments version
    print(f"\nAttempting update for {target_id} without explicit version...")
    update_payload_no_version = DocumentUpdate(
        updates={
            "description": "This document has been modified."
        }
    )
    try:
        response = conditional_update(table_name, target_id, update_payload_no_version)
        print("Update without explicit version response:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error during update without explicit version: {e}")
