import json

from database_client import get_container
from database_models import QueryDocumentsRequest


def query_documents(field_name: str, field_value):
    container = get_container()
    req = QueryDocumentsRequest(field_name=field_name, field_value=field_value)
    query = f"SELECT * FROM c WHERE c.{req.field_name} = @value"
    params = [{"name": "@value", "value": req.field_value}]
    return list(
        container.query_items(
            query=query, parameters=params, enable_cross_partition_query=True
        )
    )


def main(payload: str) -> str:
    data = json.loads(payload)
    return json.dumps(query_documents(data["field_name"], data["field_value"]))
