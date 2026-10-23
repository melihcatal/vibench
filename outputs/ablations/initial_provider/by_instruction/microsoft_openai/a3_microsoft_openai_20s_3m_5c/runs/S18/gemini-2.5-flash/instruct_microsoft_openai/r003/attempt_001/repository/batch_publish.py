import uuid
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from messaging_client import MessagingClient
from messaging_models import EventMessage

def batch_publish(topic_name: str, event_data_list: list[dict]):
    messaging_client = MessagingClient()
    sender = messaging_client.get_sender(topic_name)

    messages_to_send = []
    for data in event_data_list:
        event = EventMessage(
            event_id=str(uuid.uuid4()),
            event_type="com.example.event.batch",
            source="batch_publish.py",
            timestamp=datetime.now().isoformat(),
            data=data,
            attributes={"batch_item_count": str(len(event_data_list))}
        )
        messages_to_send.append(ServiceBusMessage(event.to_json_string()))

    sender.send_messages(messages_to_send)
    sender.close()
    print(f"Published a batch of {len(messages_to_send)} events to {topic_name}.")
