import os
import uuid
from datetime import datetime
from openai import OpenAI
from azure.servicebus import ServiceBusMessage
from messaging_client import MessagingClient
from messaging_models import EventMessage

def publish_event(topic_name: str, event_data: dict, openai_prompt: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messaging_client = MessagingClient()
    sender = messaging_client.get_sender(topic_name)

    # Use OpenAI to process the prompt
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": openai_prompt}
        ]
    )
    processed_content = response.choices[0].message.content

    event = EventMessage(
        event_id=str(uuid.uuid4()),
        event_type="com.example.event.processed",
        source="publish_event.py",
        timestamp=datetime.now().isoformat(),
        data={"original_data": event_data, "processed_content": processed_content},
        attributes={
            "content_length": str(len(processed_content)),
            "openai_model": "gpt-4o"
        }
    )

    message = ServiceBusMessage(event.to_json_string())
    sender.send_messages(message)
    sender.close()
    print(f"Event {event.event_id} published to {topic_name} with processed content from OpenAI.")

