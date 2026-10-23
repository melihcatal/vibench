from azure.cosmos import CosmosClient

from messaging_client import load_messaging_config


def message_audit_store(record, config=None):
    cfg = load_messaging_config(config)
    client = CosmosClient(cfg.get("cosmos_url", "https://example.documents.azure.com:443/"), credential=cfg.get("cosmos_key", ""))
    container = client.get_database_client(cfg.get("cosmos_database", "messages")).get_container_client(cfg.get("cosmos_container", "audit"))
    container.upsert_item(record)
    return {"stored": True, "id": record.get("id")}
