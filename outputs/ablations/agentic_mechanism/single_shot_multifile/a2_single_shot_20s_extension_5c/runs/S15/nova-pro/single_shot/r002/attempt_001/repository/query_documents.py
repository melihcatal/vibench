from database_client import DatabaseClient
from database_models import Document

def query_documents(field, value):
    client = DatabaseClient()
    container = client.get_container()
    query = f'SELECT * FROM c WHERE c.{field} = "{value}"'
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return [Document.from_dict(item) for item in items]