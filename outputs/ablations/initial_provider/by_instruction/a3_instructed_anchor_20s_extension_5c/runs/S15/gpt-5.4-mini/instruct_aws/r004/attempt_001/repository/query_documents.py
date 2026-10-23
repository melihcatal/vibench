import json
import os

from boto3.dynamodb.conditions import Attr, Key

from database_client import table
from database_models import query_result


def query_documents(field_name, field_value):
    if field_name == "id":
        response = table().query(KeyConditionExpression=Key("id").eq(str(field_value)))
    else:
        response = table().scan(FilterExpression=Attr(field_name).eq(field_value))
    return query_result(response.get("Items", []))


def main():
    field_name = os.environ.get("QUERY_FIELD", "id")
    field_value = os.environ.get("QUERY_VALUE", "")
    print(json.dumps(query_documents(field_name, field_value)))


if __name__ == "__main__":
    main()
