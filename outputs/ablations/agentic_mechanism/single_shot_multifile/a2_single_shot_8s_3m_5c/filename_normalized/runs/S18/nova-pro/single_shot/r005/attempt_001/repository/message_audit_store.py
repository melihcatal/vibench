from google.cloud import datastore

client = datastore.Client()

key = client.key('MessageAudit', 'unique_id')
entity = datastore.Entity(key=key)
entity.update({'processed_at': datetime.datetime.utcnow()})
client.put(entity)