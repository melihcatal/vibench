from messaging_client import get_gemini_client
from messaging_models import EventMessage
import json


def summarize_message_content(message: EventMessage) -> str:
    model = get_gemini_client()
    message_text = f"Message ID: {message.id}\nMessage Data: {json.dumps(message.data)}\nAttributes: {json.dumps(message.attributes or {})}"
    prompt = f"Summarize the following message content:\n\n{message_text}"
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    pass
