from database_client import get_container
from database_models import DocumentQueryRequest


def query_documents(request: DocumentQueryRequest) -> list[dict]:
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    items = container.query_items(
        query=query,
        parameters=[{"name": "@value", "value": request.field_value}],
        enable_cross_partition_query=True,
    )
    return list(items)
