import json

from azure.cosmos import CosmosClient


def store_message_record(record: dict) -> dict:
    client = CosmosClient(os.environ["AZURE_COSMOS_ENDPOINT"], credential=os.environ["AZURE_COSMOS_KEY"])
    database = client.get_database_client(os.environ["AZURE_COSMOS_DATABASE"])
    container = database.get_container_client(os.environ["AZURE_COSMOS_CONTAINER"])
    container.upsert_item(record)
    return {"stored": True, "id": record.get("id")}


if __name__ == "__main__":
    import os
    print(json.dumps(store_message_record({"id": "audit-1"})))
