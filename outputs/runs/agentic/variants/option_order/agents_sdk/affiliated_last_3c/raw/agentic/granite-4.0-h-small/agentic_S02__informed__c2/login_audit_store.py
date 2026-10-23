import os
import json
from identity_client import store_login_event, NormalizedClaims, AuthTokenSet
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

def persist_federated_login_audit(auth_response: dict, normalized_claims: NormalizedClaims):
    """Persist audit records for a completed federated login.

    Parameters:
        auth_response (dict): Raw token response from the identity provider (MSAL, Google, etc.).
        normalized_claims (NormalizedClaims): Structured claim data ready for storage.
    """
    # Verify configuration – Azure Cosmos DB is used as the managed NoSQL document store.
    COSMOS_URI = os.getenv('AZURE_COSMOS_URI')
    COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')
    DATABASE = os.getenv('AZURE_COSMOS_DATABASE')
    CONTAINER = os.getenv('AZURE_COSMOS_CONTAINER')
    if not all([COSMOS_URI, COSMOS_KEY, DATABASE, CONTAINER]):
        raise RuntimeError('Cosmos DB credentials are missing in the environment')

    credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_URI, credential=credential)
    db = client.get_database_client(DATABASE)
    container = db.get_container_client(CONTAINER)

    # Build a LoginEvent document
    event = {
        'id': str(uuid.uuid4()),
        'user_id': normalized_claims.sub,
        'source': auth_response.get('id_token_claims', {}).get('iss', 'unknown'),
        'timestamp': auth_response.get('expires_at_iso', ''),  # optional external timestamp
        'claims': json.loads(json.dumps(normalized_claims)),  # ensure serializable
    }
    # Include raw token payload for full audit trace (optional)
    raw_tokens = {
        'access_token': auth_response.get('access_token'),
        'id_token': auth_response.get('id_token'),
        'refresh_token': auth_response.get('refresh_token'),
    }
    event['raw_tokens'] = raw_tokens

    container.upsert_item(event)
    print(f'Logged event {event["id"]} to Cosmos DB.')

    # Example of reading back the most recent entry for verification
    query = container.query_items(
        query='SELECT TOP 1 * FROM c ORDER BY c.timestamp DESC',
        parameters=[]
    )
    recent = next(query, None)
    if recent:
        print('Most recent audit stored:', json.dumps(recent, indent=2))

if __name__ == '__main__':
    # Demo payload – in real usage you would receive this from oauth_callback.py
    demo_auth_response = {
        'access_token': 'ya29.a0AfH6SM-...example_token...-123456',
        'id_token': json.dumps({
            'sub': 'user-001',
            'name': 'Alice Example',
            'email': 'alice@example.com',
        }),
        'expires_at_iso': '2025-09-01T12:00:00Z',
    }
    claims = NormalizedClaims(
        sub='user-001',
        name='Alice Example',
        email='alice@example.com',
        given_name='Alice',
        family_name='Example',
    )
    persist_federated_login_audit(demo_auth_response, claims)
