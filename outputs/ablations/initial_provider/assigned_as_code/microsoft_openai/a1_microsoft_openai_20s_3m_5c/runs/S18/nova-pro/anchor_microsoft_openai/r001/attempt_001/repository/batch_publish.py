import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def batch_publish(payloads, config):
    client = ServiceBusClient.from_connection_string(config['connection_string'])
    with client:
        sender = client.get_topic_sender(topic_name=config['topic'])
        with sender:
            for payload in payloads:
                sender.send_messages(ServiceBusMessage(json.dumps(payload['event']), message_id=payload['id'], content_type='application/json'))

if __name__ == '__main__':
    payloads = [
        {'id': '1', 'event': {'data': 'Event 1'}},
        {'id': '2', 'event': {'data': 'Event 2'}},
        {'id': '3', 'event': {'data': 'Event 3'}}
    ]
    config = {
        'connection_string': 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>',
        'topic': 'my-topic'
    }
    batch_publish(payloads, config)