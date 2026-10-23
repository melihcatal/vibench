import json
import os
from ibm_cloudant import CloudantClient
from ibm_cloudant.cloudant.errors import CloudantClientError

class CloudantProfileNoteStore:
    def __init__(self):
        auth_url = os.getenv('IBM_CLOUDANT_URL')
        api_key = os.getenv('IBM_CLOUDANT_APIKEY')
        self.client = CloudantClient(url=auth_url, auth=f'{api_key}', api_key=api_key)
        self.db = self.client.create_database('onboarding_notes', throw_on_exists=False)

    def store_note(self, user_id: str, note_data: dict) -> dict:
        design = {
            '_id': '_design/notes',
            'views': {
                'by_user': {
                    'map': 'function(doc) { if (doc.user_id) { emit(doc.user_id, doc); } }'
                }
            }
        }
        # Ensure design doc exists (simple check)
        try:
            self.db.get(design['_id'])
        except CloudantClientError:
            self.db.insert(design)
        # Insert note with current timestamp
        note_data['_id'] = f'{user_id}_{int(os.getenv("TIMESTAMP", time.time()))}'
        result = self.db.create_document(note_data)
        return result.to_dict()

# Singleton instance for reuse
profile_note_store = CloudantProfileNoteStore()

def persist_onboarding_note(user_id: str, note_text: str, support_metadata: dict) -> dict:
    note = {
        'user_id': user_id,
        'note': note_text,
        'metadata': support_metadata,
        'created_at': int(os.getenv('TIMESTAMP', '0'))
    }
    return profile_note_store.store_note(user_id, note)
