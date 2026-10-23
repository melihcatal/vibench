import boto3
import os
import json

def conditional_update_document(
    table_name: str,
    key: dict,
    update_expression: str,
    expression_attribute_values: dict,
    condition_expression: str
):
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        key (dict): A dictionary representing the primary key of the item to update.
                    Example: {"id": "document123"}
        update_expression (str): The update expression to apply.
                                 Example: "SET #attr = :value"
        expression_attribute_values (dict): A dictionary of values for the expression.
                                            Example: {":value": "new_value"}
        condition_expression (str): The condition expression that must be satisfied for the update to proceed.
                                    Example: "attribute_exists(id)" or "version = :current_version"
    Returns:
        dict: The response from the DynamoDB update_item operation.
    """
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    table = dynamodb.Table(table_name)

    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression,
        ReturnValues="ALL_NEW"
    )
    return response

if __name__ == "__main__":
    # Example usage (replace with your actual table name and data)
    # Ensure you have AWS credentials configured in your environment or ~/.aws/credentials
    # and AWS_REGION set.
    # For local testing, you can use DynamoDB Local:
    # `docker run -p 8000:8000 amazon/dynamodb-local`

    # os.environ["AWS_REGION"] = "us-east-1" # Set your desired region
    # os.environ["DYNAMODB_ENDPOINT_URL"] = "http://localhost:8000" # Uncomment for DynamoDB Local

    # Example 1: Conditional update - only update if 'status' is 'pending'
    # table_name = "MyDocuments"
    # document_key = {"document_id": "doc123"}
    # update_expr = "SET #st = :new_status"
    # expr_attr_values = {":new_status": "processed"}
    # cond_expr = "#st = :expected_status"
    # expr_attr_names = {"#st": "status"} # For attribute names that might conflict with reserved words

    # # If you need to use ExpressionAttributeNames, include them in the update_item call
    # # response = conditional_update_document(
    # #     table_name,
    # #     document_key,
    # #     update_expr,
    # #     {**expr_attr_values, ":expected_status": "pending"},
    # #     cond_expr,
    # #     ExpressionAttributeNames=expr_attr_names
    # # )
    # # print(f"Conditional Update Response 1: {json.dumps(response, indent=2)}")

    pass
