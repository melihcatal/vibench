from security_client import get_mistral_client
from security_models import SummarizeRequest, SummarizeResponse


def summarize_key_usage(request: SummarizeRequest) -> SummarizeResponse:
    client = get_mistral_client()
    chat_response = client.chat(
        model="mistral-tiny",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following key usage and crypto events concisely: {request.text}",
            }
        ],
    )
    summary = chat_response.choices[0].message.content
    return SummarizeResponse(summary=summary)
