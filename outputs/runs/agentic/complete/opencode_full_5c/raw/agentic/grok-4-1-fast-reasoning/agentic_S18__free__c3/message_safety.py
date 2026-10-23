import os
import json
from openai import OpenAI
from messaging_models import PubSubMessage


def is_safe(message: PubSubMessage) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = json.dumps(message.payload)
    if len(text) > 100000:
        text = text[:100000]
    response = client.moderations.create(input=text)
    return not response.results[0].flagged
