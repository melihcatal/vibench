import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def dead_letter(payload, config):
    client = ServiceBusClient.from_connection_string(config['connection_string'])
    with client:
        sender = client.get_queue_sender(queue_name=config['dead_letter_queue'])
        with sender:
            sender.send_messages(ServiceBusMessage(json.dumps(payload)))

if __name__ == '__main__':
    payload = {'error': 'Failed to process message'}
    config = {
        'connection_string': 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>',
        'dead_letter_queue': 'dead-letter-queue'
    }
    dead_letter(payload, config)