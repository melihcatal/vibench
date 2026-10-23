import json
from database_client import NoSQLClient

def query_documents(field, value):
    """Query documents where `field` equals `value`.

    Uses Azure Cosmos DB for NoSQL with SQL query syntax.
    """
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    query = f"SELECT * FROM c WHERE c.{field} = @value"
    options = {'parameters': [{'name': '@value', 'value': value}]}  # Cosmos DB parameterized query
    result = container.query_items(query=query, options=options)
    return list(result)
