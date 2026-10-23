import os
import json
from google.cloud import datastore

class ProfileNoteStore:
    """Facade for persisting onboarding notes and support metadata.
    Uses Google Cloud Datastore as the managed document store.
    """
    def __init__(self):
        self.client = datastore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
        self.kind = 'ProfileNote'
    
    def persist(self, user_id: str, payload: dict):
        """Store a JSON-serializable payload with a timestamp.
        Returns the Datastore key identifier.
        """
        key = self.client.key(self.kind, user_id)
        note = self.client.entity(key)
        note['user_id'] = user_id
        note['payload'] = json.dumps(payload)
        note['timestamp'] = datetime.datetime.utcnow()
        self.client.put(note)
        return {'kind': self.kind, 'id': user_id}

# Singleton convenience (optional)
NOTE_STORE = ProfileNoteStore()
