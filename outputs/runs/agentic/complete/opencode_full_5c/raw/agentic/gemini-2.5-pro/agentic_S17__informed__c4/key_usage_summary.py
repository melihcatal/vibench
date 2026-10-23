import os
import openai
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    """
    Summarize key usage and crypto events using OpenAI's GPT model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not request.events:
        return KeyUsageSummaryResponse(summary="No events to summarize.")

    prompt = (
        "Summarize the following cryptographic key usage events in a brief report:\n\n"
    )
    for event in request.events:
        prompt += f"- {event}\n"

    prompt += "\nSummary:"

    client = openai.OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    summary = chat_completion.choices[0].message.content
    return KeyUsageSummaryResponse(summary=summary.strip())
