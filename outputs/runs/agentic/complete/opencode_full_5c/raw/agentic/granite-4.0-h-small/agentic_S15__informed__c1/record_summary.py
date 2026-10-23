# [LATER-STEP] record_summary.py

# Example using watsonx.ai Text Chat for summarization
# Identifier: Service = watsonx.ai text chat, SDK = ibm-watsonx-ai

from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceInstanceType


def summarize_record(record: dict) -> str:
    """Generate a concise summary of a retrieved document record.

    Args:
        record (dict): The full document dictionary from the NoSQL store.

    Returns:
        str: A short summary of the document's main content.
    """
    # Initialize the watsonx client (uses env vars WATSONX_API_KEY, WATSONX_PROJECT_ID)
    wxa_client = Client(instance_type=ServiceInstanceType.WATSONX_AI)

    # Prompt template for summarization
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{record.get('content', '')}"

    # Call the watsonx text chat endpoint
    assistant_reply = wxa_client.conversational_ai.chat(
        project_id=wxa_client.get_default_project_id(),
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract assistant message content
    summary = assistant_reply[0]["content"]
    return summary
