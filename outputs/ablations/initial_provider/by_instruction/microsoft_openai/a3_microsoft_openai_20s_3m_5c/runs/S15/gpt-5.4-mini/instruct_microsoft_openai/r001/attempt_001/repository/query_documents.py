from database_client import get_container
from database_models import QueryDocumentsRequest


def query_documents(request: QueryDocumentsRequest):
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    items = container.query_items(
        query=query,
        parameters=[{"name": "@value", "value": request.field_value}],
        enable_cross_partition_query=request.partition_key is None,
    )
    return list(items)
