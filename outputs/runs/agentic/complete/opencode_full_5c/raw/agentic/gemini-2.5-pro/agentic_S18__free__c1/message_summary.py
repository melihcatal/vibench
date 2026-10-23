from typing import List
from messaging_client import get_openai_client
from messaging_models import ProcessedMessage


def summarize_messages(messages: List[ProcessedMessage]) -> str:
    client = get_openai_client()

    if not messages:
        return "No messages to summarize."

    texts_to_summarize = "\n".join(
        [f"- {msg.original_payload.text}" for msg in messages]
    )

    prompt = (
        f"Summarize the following messages in a single paragraph:\n{texts_to_summarize}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes messages.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()
