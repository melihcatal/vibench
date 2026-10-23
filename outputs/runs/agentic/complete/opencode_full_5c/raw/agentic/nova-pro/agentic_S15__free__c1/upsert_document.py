import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

table_name = "ManagedNoSQLStore"


def upsert_document(primary_id, document):
    table = dynamodb.Table(table_name)
    table.put_item(Item={**document, "id": primary_id})
    print(f"Document with ID {primary_id} upserted successfully.")
