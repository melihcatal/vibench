import os
from database_client import get_client
from database_models import DocumentModel

def query_documents(field_name, field_value):
    """Query documents where a top‑level field matches the given value.
    Uses Azure Cosmos DB SQL API to run a parameterised query.
    """
    client = get_client()
    container = client["my_container"]
    sql = f"SELECT * FROM c WHERE c.{field_name} = @value"
    options = {
        "enable_cross_partition_query": False if isinstance(field_value, (int, str)) else True,
    }
    items = list(container.query_items(
        query=sql,
        parameters=[{"name": "@value", "value": field_value}],
        **options,
    ))
    return [DocumentModel.from_dict(d) for d in items]
