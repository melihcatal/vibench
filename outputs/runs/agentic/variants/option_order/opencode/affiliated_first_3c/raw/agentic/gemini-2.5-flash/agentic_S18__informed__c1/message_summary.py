import os
from messaging_client import GeminiClient
from messaging_models import Event
import json


def summarize_message_payload(event: Event) -> str:
    client = GeminiClient()

    prompt = f"Summarize the following JSON event payload in a concise sentence: {json.dumps(event.payload)}"
    response = client.model.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    # Example usage
    sample_event = Event(
        event_id="summary-test-1",
        event_type="product_review",
        payload={
            "product_name": "Wireless Headphones",
            "rating": 5,
            "review_text": "These headphones are amazing! The sound quality is superb and they are very comfortable to wear for long periods.",
        },
    )

    try:
        summary = summarize_message_payload(sample_event)
        print(f"Message payload summary: {summary}")
    except Exception as e:
        print(f"Error summarizing message: {e}")
