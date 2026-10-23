import boto3


def query_documents(table_name, key_condition):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=key_condition)
    return response.get("Items")


if __name__ == "__main__":
    print(
        query_documents(
            "my_table",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("id").eq("123"),
        )
    )
