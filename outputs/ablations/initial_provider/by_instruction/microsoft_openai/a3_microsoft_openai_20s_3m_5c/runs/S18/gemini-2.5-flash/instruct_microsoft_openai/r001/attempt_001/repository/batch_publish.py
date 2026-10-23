import os
import uuid
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from messaging_client import get_service_bus_client
from messaging_models import EventMessage

# Configuration
SERVICE_BUS_TOPIC_NAME = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")

def batch_publish_events(event_data_list: list[dict]):
    client = None
    try:
        client = get_service_bus_client(topic_name=SERVICE_BUS_TOPIC_NAME)
        sender = client.get_sender()

        service_bus_messages = []
        for event_data in event_data_list:
            event = EventMessage(
                event_id=str(uuid.uuid4()),
                event_type="com.example.batch_event",
                data=event_data,
                source="my_batch_application",
                timestamp=datetime.utcnow().isoformat()
            )
            message_body = event.to_json()
            service_bus_messages.append(ServiceBusMessage(message_body))
            print(f"Prepared event with ID: {event.event_id} for batch.")
        
        if service_bus_messages:
            sender.send_messages(service_bus_messages)
            print(f"Successfully published a batch of {len(service_bus_messages)} events.")
        else:
            print("No messages to publish in batch.")

    except Exception as e:
        print(f"Error publishing batch of events: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    # Example usage
    sample_batch_data = [
        {"order_id": "1001", "status": "new", "amount": 100.50},
        {"order_id": "1002", "status": "processing", "amount": 25.00},
        {"order_id": "1003", "status": "failed", "amount": 75.25}
    ]
    batch_publish_events(sample_batch_data)
