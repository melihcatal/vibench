from database_client import client, database_name, container_name


def conditional_update(document_id: str, new_data: Dict, etag: str):
    container = client.get_database_client(database_name).get_container_client(
        container_name
    )
    item = container.read_item(
        item=document_id, partition_key=PartitionKey(document_id)
    )
    if item["_etag"] == etag:
        container.replace_item(item=document_id, body=new_data)
    else:
        raise ValueError("Conditional update failed due to version mismatch.")
