import openai
import os
import json
from typing import Dict, Any


def is_message_safe(msg: Dict[str, Any]) -> bool:
    """
    Checks message payload text for unsafe content using OpenAI Moderation.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = json.dumps(msg.get("payload", {}))
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return not response.results[0].flagged
