from database_client import get_cosmos_client
from database_models import Document

def query_documents(field_name: str, field_value: str):
    container = get_cosmos_client()
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    parameters = [{
        "name": "@value",
        "value": field_value
    }]
    
    items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
    return [Document.from_dict(item) for item in items]
