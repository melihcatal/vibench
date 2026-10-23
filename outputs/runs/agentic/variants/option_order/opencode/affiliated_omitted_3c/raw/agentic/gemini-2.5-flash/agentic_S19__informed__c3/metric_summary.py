import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_metric_trends(metric_data: str):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following metric data, identifying any trends or anomalies: {metric_data}",
        )
    ]

    chat_response = client.chat(
        model="mistral-large-latest",
        messages=messages,
    )

    return chat_response.choices[0].message.content
