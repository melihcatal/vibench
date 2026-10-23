import json
import os

from openai import OpenAI

from messaging_client import create_client, get_topic_name
from messaging_models import build_event


def publish_event(payload):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-5.4-mini", input=str(payload))
    content = response.output_text if hasattr(response, "output_text") else str(payload)
    event = build_event("event", {"input": payload, "enriched": content})
    with create_client() as sb_client:
        sender = sb_client.get_topic_sender(topic_name=get_topic_name())
        with sender:
            sender.send_messages(json.dumps(event))
    return event
