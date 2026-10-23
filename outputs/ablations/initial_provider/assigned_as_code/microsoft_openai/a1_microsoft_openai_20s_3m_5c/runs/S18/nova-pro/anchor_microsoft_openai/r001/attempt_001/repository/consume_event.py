import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def consume_event(config):
    client = ServiceBusClient.from_connection_string(config['connection_string'])
    with client:
        receiver = client.get_subscription_receiver(topic_name=config['topic'], subscription_name=config['subscription'])
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            for msg in received_msgs:
                print(f"Received message: {msg.body}")
                receiver.complete_message(msg)

if __name__ == '__main__':
    config = {
        'connection_string': 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>',
        'topic': 'my-topic',
        'subscription': 'my-subscription'
    }
    consume_event(config)