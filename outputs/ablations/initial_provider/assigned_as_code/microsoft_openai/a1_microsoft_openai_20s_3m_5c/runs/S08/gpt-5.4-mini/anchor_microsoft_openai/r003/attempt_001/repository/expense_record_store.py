from google.cloud import firestore


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config['project_id'])
    doc = client.collection(config.get('collection', 'expense_records')).document(config['record_id'])
    doc.set(payload['record'])
    return {'stored': True, 'record_id': config['record_id']}
