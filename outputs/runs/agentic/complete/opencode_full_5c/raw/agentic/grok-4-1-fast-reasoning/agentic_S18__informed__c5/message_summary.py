import google.generativeai as genai
import os
from datetime import datetime
from uuid import uuid4
from messaging_models import MessageEvent, MessagePayload

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_summary(event: MessageEvent) -> str:
    prompt = f"Summarize this customer service message in 1-2 sentences: {event.payload.message}"
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    event = MessageEvent(
        event_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        payload=MessagePayload(
            customer_name="Jane Smith",
            order_id="ORD-456",
            message="My order arrived late and the item is incorrect. Please assist with return.",
        ),
    )
    summary = generate_summary(event)
    print(f"Summary: {summary}")
