from database_client import query_items
from database_models import DocumentQueryRequest


def query_documents(field_name, field_value):
    request = DocumentQueryRequest(field_name=field_name, field_value=field_value)
    query = f"SELECT * FROM c WHERE c.{request.field_name} = @value"
    return query_items(query, [{"name": "@value", "value": request.field_value}])
