from azure.cosmos import CosmosClient

def get_client():
    return CosmosClient('https://<your-cosmosdb-instance>.documents.azure.com:443/', credential='<your-cosmosdb-key>')

if __name__ == '__main__':
    client = get_client()