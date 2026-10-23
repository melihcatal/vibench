from botocore.exceptions import ClientError
from database_client import get_database_client, get_table_name


def fetch_document(document_id: str):
    """
    Fetches a document from DynamoDB by its ID.
    """
    dynamodb = get_database_client()
    table = dynamodb.Table(get_table_name())
    try:
        response = table.get_item(Key={"document_id": document_id})
        if "Item" in response:
            return response["Item"]
        else:
            return None
    except ClientError as e:
        print(f"Error fetching document: {e.response['Error']['Message']}")
        return None
