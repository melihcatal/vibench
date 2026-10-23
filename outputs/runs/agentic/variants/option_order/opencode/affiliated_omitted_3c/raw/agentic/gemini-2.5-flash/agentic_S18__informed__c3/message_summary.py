import json
import os
from messaging_client import AWSMessagingClient
from messaging_models import MessageSummaryRequest, MessageSummaryResult


def summarize_message(request: MessageSummaryRequest) -> MessageSummaryResult:
    """Summarizes message content using Amazon Bedrock (Anthropic Claude)."""
    bedrock_runtime = AWSMessagingClient().get_bedrock_runtime_client()
    model_id = "anthropic.claude-v2"

    prompt = f"Human: Summarize the following message content concisely:\n\n{request.message_content}\n\nAssistant:"

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0.5,
            "top_p": 0.9,
        }
    )

    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion", "No summary generated.").strip()
        return MessageSummaryResult(summary=summary)
    except Exception as e:
        print(f"Error summarizing message with Bedrock: {e}")
        return MessageSummaryResult(summary=f"Error: {e}")


if __name__ == "__main__":
    # Example Usage
    sample_message_content = (
        "A new order (ORD-2023-10-26-001) has been placed by customer 'John Doe' (ID: CUST-007) "
        "for items: [Product A (Qty: 2), Product B (Qty: 1)]. Total amount: $150.00. "
        "Payment method: Credit Card. Shipping address: 123 Main St, Anytown, USA. "
        "Status: Pending fulfillment. Notification sent to customer via email and SMS."
    )

    summary_request = MessageSummaryRequest(message_content=sample_message_content)
    summary_result = summarize_message(summary_request)
    print("\n--- Message Summary ---")
    print(f"Original: {sample_message_content}")
    print(f"Summary: {summary_result.summary}")
