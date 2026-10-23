from database_client import get_container
from database_models import DocumentResponse


def query_documents(field_name=None, field_value=None, partition_key=None):
    container = get_container()
    if partition_key is not None:
        query = "SELECT * FROM c WHERE c.partition_key = @pk"
        parameters = [{"name": "@pk", "value": partition_key}]
    else:
        query = f"SELECT * FROM c WHERE c.{field_name} = @value"
        parameters = [{"name": "@value", "value": field_value}]
    items = list(
        container.query_items(
            query=query, parameters=parameters, enable_cross_partition_query=True
        )
    )
    return DocumentResponse(ok=True, document={"items": items}).to_dict()
