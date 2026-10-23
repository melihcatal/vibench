import boto3


def upsert_document(table_name, primary_key, document):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item={primary_key: document[primary_key], "data": document})


if __name__ == "__main__":
    upsert_document("example-table", "id", {"id": "123", "data": "example data"})
