import boto3


def upsert_document(table_name, item):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


if __name__ == "__main__":
    upsert_document("my_table", {"id": "123", "name": "John Doe"})
