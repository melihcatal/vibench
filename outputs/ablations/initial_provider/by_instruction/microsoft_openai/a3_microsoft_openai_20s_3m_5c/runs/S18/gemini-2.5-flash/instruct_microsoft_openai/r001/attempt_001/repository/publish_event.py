import os
import uuid
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from messaging_client import get_service_bus_client
from messaging_models import EventMessage

# Configuration
SERVICE_BUS_TOPIC_NAME = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")

def publish_event(event_data: dict):
    client = None
    try:
        client = get_service_bus_client(topic_name=SERVICE_BUS_TOPIC_NAME)
        sender = client.get_sender()

        event = EventMessage(
            event_id=str(uuid.uuid4()),
            event_type="com.example.myevent",
            data=event_data,
            source="my_application",
            timestamp=datetime.utcnow().isoformat()
        )
        message_body = event.to_json()
        service_bus_message = ServiceBusMessage(message_body)
        
        sender.send_messages(service_bus_message)
        print(f"Published event with ID: {event.event_id}")

    except Exception as e:
        print(f"Error publishing event: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    # Example usage
    sample_event_data = {"key": "value", "message": "Hello Service Bus!"}
    publish_event(sample_event_data)
