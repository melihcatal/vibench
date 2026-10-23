from database_client import get_container_client
from database_models import build_query


def query_documents(payload, config=None):
    container = get_container_client(config)
    if 'field' in payload and 'value' in payload:
        query = build_query(payload['field'], payload['value'])
        return list(container.query_items(query=query['query'], parameters=query['parameters'], enable_cross_partition_query=True))
    return list(container.query_items(query='SELECT * FROM c WHERE c.pk = @pk', parameters=[{'name': '@pk', 'value': payload['partition_key']}], enable_cross_partition_query=True))
