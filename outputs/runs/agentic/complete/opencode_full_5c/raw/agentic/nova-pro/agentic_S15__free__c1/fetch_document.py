import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

table_name = "ManagedNoSQLStore"


def fetch_document(primary_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"id": primary_id})
    return response.get("Item", None)
