from typing import List
from identity_models import LoginAuditRecord
from azure.cosmos import CosmosClient, PartitionKey

def persist_audit_records(audit_records: List[LoginAuditRecord]) -> None:
    client = CosmosClient.from_connection_string(
        "AccountEndpoint=https://login-audit.documents.azure.com:443/;AccountKey=...")
    database = client.get_database_client("LoginAuditDB")
    container = database.get_container_client("AuditRecords")
    for record in audit_records:
        container.upsert_item(record)