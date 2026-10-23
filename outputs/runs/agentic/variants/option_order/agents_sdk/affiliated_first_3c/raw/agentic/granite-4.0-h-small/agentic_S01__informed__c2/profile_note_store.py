import os
from ibm_cloudant import Cloudant

# IBM Cloudant (managed NoSQL) as the concrete document store
CLOUDANT_URL = os.getenv('IBM_CLOUDANT_URL')
CLOUDANT_APIKEY = os.getenv('IBM_CLOUDANT_APIKEY')

def init_cloudant() -> Cloudant.client.CloudantClient:
    """Create and return a Cloudant client using IAM API key."""
    if not CLOUDANT_URL or not CLOUDANT_APIKEY:
        raise RuntimeError('Missing Cloudant credentials')
    client = Cloudant.client(url=CLOUDANT_URL, username='apikey', password=CLOUDANT_APIKEY)
    return client


def store_onboarding_note(user_id: str, note: dict):
    """Persist onboarding note/metadata under user_id in Cloudant."""
    client = init_cloudant()
    # Use a database named after the application (you could also namespace by tenant)
    db = client.get_database('onboarding_notes', auto_create_database=True)
    # Ensure a document ID, fallback to UUID if not supplied
    note_id = note.get('_id') or str(uuid.uuid4())
    note['_id'] = note_id
    # Optional: tag with user_id for later lookup
    note['user_id'] = user_id
    # Write document
    db.create_document(note)
