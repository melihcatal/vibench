from azure.cosmos import CosmosClient


def profile_note_store(note: dict):
    client = CosmosClient.from_connection_string("AZURE_COSMOS_CONNECTION_STRING")
    database = client.get_database_client("onboarding")
    container = database.get_container_client("profile_notes")
    return container.upsert_item(note)
