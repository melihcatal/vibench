import json
import os

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import make_response


def query_documents(field_name, field_value):
    table = get_table()
    result = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return make_response(True, data=result.get("Items", []))


if __name__ == "__main__":
    print(
        json.dumps(
            query_documents(
                os.environ.get("FIELD_NAME", ""), os.environ.get("FIELD_VALUE", "")
            )
        )
    )
