import os
from google.cloud import pubsub_v1

_client_cache = {}

def get_pubsub_client(client_type: str = "publisher") -> pubsub_v1.PublisherClient | pubsub_v1.SubscriberClient:
    cache_key = f"{client_type}_client"
    
    if cache_key not in _client_cache:
        if client_type == "publisher":
            _client_cache[cache_key] = pubsub_v1.PublisherClient()
        elif client_type == "subscriber":
            _client_cache[cache_key] = pubsub_v1.SubscriberClient()
        else:
            raise ValueError(f"Unknown client type: {client_type}")
    
    return _client_cache[cache_key]