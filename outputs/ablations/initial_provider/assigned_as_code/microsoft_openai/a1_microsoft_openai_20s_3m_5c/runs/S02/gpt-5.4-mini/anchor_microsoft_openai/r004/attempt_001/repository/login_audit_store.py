from google.cloud import firestore


def login_audit_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get('project_id'))
    collection = config.get('collection', 'login_audit')
    doc = client.collection(collection).document()
    record = dict(payload)
    doc.set(record)
    return {'document_id': doc.id, 'stored': True}
