from azure.eventhub import EventHubProducerClient, EventData

def batch_publish(events):
    client = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>;EntityPath=<eventHubName>")
    event_data_batch = client.create_batch()
    for event in events:
        event_data_batch.add(EventData(event))
    client.send_batch(event_data_batch)
    client.close()