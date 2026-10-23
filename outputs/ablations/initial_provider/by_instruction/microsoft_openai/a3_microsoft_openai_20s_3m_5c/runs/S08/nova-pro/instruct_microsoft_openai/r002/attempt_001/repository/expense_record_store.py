from azure.cosmos import CosmosClient

def store_expense_record(expense_record):
    client = CosmosClient("https://<your-cosmos-db-endpoint>.documents.azure.com:443/", credential="<your-cosmos-db-key>")
    database = client.get_database_client("expenseDb")
    container = database.get_container_client("expenseContainer")
    container.upsert_item(expense_record)