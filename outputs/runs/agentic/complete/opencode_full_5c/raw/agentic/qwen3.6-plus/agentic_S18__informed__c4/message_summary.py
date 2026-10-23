import os
import json
from openai import OpenAI
from messaging_models import PubSubEvent, ConsumeResult


def summarize_message(result: ConsumeResult, model: str = "gpt-4o-mini") -> dict:
    event = result.to_event()
    if event is None:
        return {"error": "No valid event to summarize", "summary": None}

    payload_text = json.dumps(event.payload, indent=2)
    attributes_text = json.dumps(event.attributes, indent=2)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = (
        f"Summarize the following message processing result.\n\n"
        f"Event Type: {event.event_type}\n"
        f"Source: {event.source}\n"
        f"Event ID: {event.event_id}\n"
        f"Timestamp: {event.timestamp}\n"
        f"Payload:\n{payload_text}\n"
        f"Attributes:\n{attributes_text}\n"
        f"Delivery Attempt: {result.delivery_attempt}\n"
        f"Message ID: {result.message_id}\n\n"
        f"Provide a concise summary of what this message represents and any notable details."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a message processing assistant. Summarize event messages clearly and concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=256,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "event_id": event.event_id,
        "message_id": result.message_id,
        "event_type": event.event_type,
        "summary": summary_text,
        "model_used": model,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
    }


if __name__ == "__main__":
    from messaging_models import ConsumeResult, PubSubEvent

    evt = PubSubEvent(
        event_type="order.created",
        source="order-service",
        payload={
            "order_id": "ORD-12345",
            "amount": 99.99,
            "items": ["Widget A", "Widget B"],
        },
    )
    cr = ConsumeResult(message_id="msg-001", event=evt)
    summary = summarize_message(cr)
    print(json.dumps(summary, indent=2))
