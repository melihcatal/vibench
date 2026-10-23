import os
from openai import OpenAI
from messaging_models import AuditEvent

def summarize_message_processing(events: list[AuditEvent]) -> str:
    """
    Summarizes a list of message processing audit events using OpenAI.

    Args:
        events: A list of AuditEvent objects.

    Returns:
        A text summary of the processing results.
    """
    if not events:
        return "No events to summarize."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)

    success_count = sum(1 for e in events if e.status == 'success')
    failure_count = len(events) - success_count
    
    prompt_content = (
        f"Summarize the following message processing results. "
        f"Total messages: {len(events)}. "
        f"Succeeded: {success_count}. Failed: {failure_count}. "
        f"Provide a brief, human-readable summary of the overall status."
    )

    if failure_count > 0:
        errors = [e.error_message for e in events if e.error_message]
        prompt_content += "\nKey errors observed: " + "; ".join(set(errors[:3]))


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes operational data.",
            },
            {
                "role": "user",
                "content": prompt_content,
            },
        ],
        model="gpt-4o",
    )

    summary = chat_completion.choices[0].message.content
    return summary if summary else "Failed to generate summary."
