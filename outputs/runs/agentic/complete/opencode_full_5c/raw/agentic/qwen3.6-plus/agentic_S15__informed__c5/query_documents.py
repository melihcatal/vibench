import os
from boto3.dynamodb.conditions import Attr
from database_client import get_table, deserialize_item
from database_models import QueryResult


def query_documents(
    field_name,
    field_value,
    table_name=None,
    partition_key="document_id",
    index_name=None,
    limit=50,
):
    table = get_table(table_name)

    filter_expr = Attr(field_name).eq(field_value)

    kwargs = {
        "FilterExpression": filter_expr,
        "Limit": limit,
    }
    if index_name:
        kwargs["IndexName"] = index_name

    try:
        response = table.scan(**kwargs)
        items = [deserialize_item(item) for item in response.get("Items", [])]
        result_items = []
        for item in items:
            doc_resp = DocumentResponse.from_dynamodb_item(item, partition_key)
            result_items.append(doc_resp)
        return QueryResult(
            items=result_items,
            count=len(result_items),
            last_evaluated_key=response.get("LastEvaluatedKey"),
        )
    except Exception:
        return QueryResult(items=[], count=0)


from database_models import DocumentResponse
