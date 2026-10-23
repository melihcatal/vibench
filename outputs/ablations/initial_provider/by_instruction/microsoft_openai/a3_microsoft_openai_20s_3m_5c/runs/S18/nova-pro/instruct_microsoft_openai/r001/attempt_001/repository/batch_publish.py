import os
from azure.eventhub import EventHubProducerClient, EventData

# Initialize the Event Hubs client
client = EventHubProducerClient.from_connection_string(conn_str=os.getenv('EVENT_HUB_CONN_STR'), eventhub_name=os.getenv('EVENT_HUB_NAME'))

# Function to publish a batch of events
def publish_batch(events):
    try:
        # Create a batch
        event_data_batch = client.create_batch()
        # Add events to the batch
        for event in events:
            event_data_batch.add(EventData(event))
        # Send the batch
        client.send_batch(event_data_batch)
        print('Batch published successfully')
    except Exception as e:
        print(f'Error publishing batch: {e}')
    finally:
        client.close()

# Example batch of events
batch_events = ['{"key": "value1"}', '{"key": "value2"}']
publish_batch(batch_events)