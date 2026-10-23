from azure.cosmos import CosmosClient, PartitionKey
from identity_models import AuditEvent
import os
import uuid

def get_cosmos_container():
    endpoint = os.getenv('COSMOS_ENDPOINT')
    key = os.getenv('COSMOS_KEY')
    client = CosmosClient(endpoint, key)
    database_name = os.getenv('COSMOS_DATABASE', 'FederatedLoginDB')
    container_name = os.getenv('COSMOS_CONTAINER', 'AuditEvents')
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/provider"),
    )
    return container

def store_audit_event(event: AuditEvent):
    container = get_cosmos_container()
    event_dict = event.dict()
    event_dict['id'] = str(uuid.uuid4())
    container.create_item(body=event_dict)
    return event_dict['id']