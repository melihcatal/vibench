from database_client import client, database_name, container_name
from database_models import Document


def upsert_document(document: Document):
    container = client.get_database_client(database_name).get_container_client(
        container_name
    )
    container.upsert_item(body=document.data, partition_key=PartitionKey(document.id))
