from pinecone import Pinecone

from identity_client import load_identity_config


def profile_note_store(payload, config=None):
    config = load_identity_config(config)
    payload = payload or {}
    pc = Pinecone(api_key=config.pinecone_api_key)
    index = pc.Index(config.pinecone_index)
    index.upsert(vectors=[{'id': payload.get('note_id', 'note'), 'values': [0.0], 'metadata': payload}])
    return {'stored': True, 'note_id': payload.get('note_id', 'note')}
