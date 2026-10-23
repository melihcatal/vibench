from database_client import get_container
from database_models import build_query_filter, normalize_document


def query_documents(payload, config=None):
    container = get_container(config)
    field = payload['field']
    value = payload['value']
    query_filter = build_query_filter(field, value)
    query = 'SELECT * FROM c WHERE c.{0} = @value'.format(query_filter['field'])
    items = list(container.query_items(query=query, parameters=[{'name': '@value', 'value': query_filter['value']}], enable_cross_partition_query=True))
    return {'documents': [normalize_document(item) for item in items]}
