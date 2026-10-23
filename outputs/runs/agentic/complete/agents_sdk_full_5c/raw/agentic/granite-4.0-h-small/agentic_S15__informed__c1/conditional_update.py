import os
from database_client import get_dynamodb_client
from database_models import Document

# Managed NoSQL store: Amazon DynamoDB

def conditional_update(doc_id: str, update_body: dict, version_expected: str) -> None:
    """Perform an atomic conditional (version-aware) update of a document.

    update_body: dictionary of attribute updates (e.g., {'title': {'Action': 'PUT', 'Value': 'New Title'}})
    version_expected: expected value of the attribute used for versioning (e.g., the current version string).
    """
    client = get_dynamodb_client()
    # DynamoDB conditional expression to ensure version matches
    expression = f"#v = :expected"
    expression_names = {'#v': 'version'}
    expression_values = {':expected': {'S': version_expected}}
    update_expression = f"SET {', '.join([f'#n = :v' for n, v in update_body.items()])}"
    client.update_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': doc_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeNames={
            '#n': None,
            **expression_names
        },
        ExpressionAttributeValues={
            **expression_values,
            **{f':v{n}': {'S': v} for n, v in update_body.items()}
        },
        ConditionExpression=expression
    )

if __name__ == "__main__":
    # Example: set title if current version is '1'
    conditional_update('test-doc-1', {'title': {'Action': 'PUT', 'Value': 'Updated Title'}}, '1')
