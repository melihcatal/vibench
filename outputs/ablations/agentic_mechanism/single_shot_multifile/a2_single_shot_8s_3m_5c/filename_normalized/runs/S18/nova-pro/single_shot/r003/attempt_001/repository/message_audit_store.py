import os
from google.cloud import datastore

client = datastore.Client()

def store_message_record(message_id, message_data):
    key = client.key('Message', message_id)
    entity = datastore.Entity(key=key)
    entity.update(message_data)
    client.put(entity)