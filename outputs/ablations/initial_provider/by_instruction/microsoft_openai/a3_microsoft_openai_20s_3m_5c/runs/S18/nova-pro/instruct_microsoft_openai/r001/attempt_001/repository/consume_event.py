import os
from azure.eventhub import EventHubConsumerClient

# Initialize the Event Hubs client
client = EventHubConsumerClient.from_connection_string(conn_str=os.getenv('EVENT_HUB_CONN_STR'), consumer_group='$Default', eventhub_name=os.getenv('EVENT_HUB_NAME'))

# Function to consume an event
def on_event(partition_context, event):
    print(f'Received event: {event.body_as_str()}')
    partition_context.update_checkpoint(event)

# Start receiving events
client.receive(on_event=on_event, starting_position='-1')
client.close()