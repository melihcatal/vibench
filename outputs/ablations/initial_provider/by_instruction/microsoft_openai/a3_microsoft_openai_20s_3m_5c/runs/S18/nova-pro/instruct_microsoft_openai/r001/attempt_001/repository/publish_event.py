import os
from azure.eventhub import EventHubProducerClient, EventData

# Initialize the Event Hubs client
client = EventHubProducerClient.from_connection_string(conn_str=os.getenv('EVENT_HUB_CONN_STR'), eventhub_name=os.getenv('EVENT_HUB_NAME'))

# Function to publish an event
def publish_event(event):
    try:
        # Create a batch
        event_data_batch = client.create_batch()
        # Add the event to the batch
        event_data_batch.add(EventData(event))
        # Send the batch
        client.send_batch(event_data_batch)
        print('Event published successfully')
    except Exception as e:
        print(f'Error publishing event: {e}')
    finally:
        client.close()

# Example event
event = '{"key": "value"}'
publish_event(event)