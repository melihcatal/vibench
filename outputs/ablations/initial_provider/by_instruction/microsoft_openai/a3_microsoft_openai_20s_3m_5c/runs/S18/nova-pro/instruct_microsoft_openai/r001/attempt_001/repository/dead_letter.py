import os
from azure.eventhub import EventHubProducerClient, EventData

# Initialize the Event Hubs client for dead-letter queue
client = EventHubProducerClient.from_connection_string(conn_str=os.getenv('EVENT_HUB_CONN_STR'), eventhub_name=os.getenv('DEAD_LETTER_QUEUE_NAME'))

# Function to send a failed message to the dead-letter queue
def send_to_dead_letter(message):
    try:
        # Create a batch
        event_data_batch = client.create_batch()
        # Add the message to the batch
        event_data_batch.add(EventData(message))
        # Send the batch
        client.send_batch(event_data_batch)
        print('Message sent to dead-letter queue successfully')
    except Exception as e:
        print(f'Error sending message to dead-letter queue: {e}')
    finally:
        client.close()

# Example failed message
failed_message = '{"error": "Failed to process"}'
send_to_dead_letter(failed_message)