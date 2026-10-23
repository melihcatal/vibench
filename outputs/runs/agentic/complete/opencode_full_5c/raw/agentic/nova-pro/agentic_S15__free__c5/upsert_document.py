import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def upsert_document(table_name, item):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    return response
