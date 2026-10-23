import os
from azure.eventhub import EventHubProducerClient, EventData

# Function to get the Event Hubs client
def get_event_hub_client():
    conn_str = os.getenv('EVENT_HUB_CONN_STR')
    eventhub_name = os.getenv('EVENT_HUB_NAME')
    return EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=eventhub_name)