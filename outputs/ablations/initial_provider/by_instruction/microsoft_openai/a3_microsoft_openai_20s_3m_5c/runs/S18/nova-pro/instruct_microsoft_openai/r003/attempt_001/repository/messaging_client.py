from azure.eventhub import EventHubProducerClient, EventHubConsumerClient

def get_producer_client():
    return EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>;EntityPath=<eventHubName>")

def get_consumer_client():
    return EventHubConsumerClient.from_connection_string(conn_str="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>;EntityPath=<eventHubName>")