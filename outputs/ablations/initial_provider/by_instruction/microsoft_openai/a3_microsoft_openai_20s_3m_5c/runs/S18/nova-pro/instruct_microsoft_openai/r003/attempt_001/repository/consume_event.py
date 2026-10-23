from azure.eventhub import EventHubConsumerClient

def consume_event():
    client = EventHubConsumerClient.from_connection_string(conn_str="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>;EntityPath=<eventHubName>")
    with client:
        received_events = client.receive(on_event=on_event, starting_position="-1")
        for event in received_events:
            print("Received event: ", event.body_as_str())

def on_event(event):
    print("Received event: ", event.body_as_str())