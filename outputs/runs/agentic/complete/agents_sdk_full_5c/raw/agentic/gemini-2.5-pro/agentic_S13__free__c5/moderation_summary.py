from safety_client import get_anthropic_client
from safety_models import SummaryRequest, SummaryResponse

def moderation_summary(request: SummaryRequest) -> SummaryResponse:
    """
    Summarizes a list of moderation decisions using Anthropic's Claude model.

    Args:
        request: A SummaryRequest object containing a list of decisions.

    Returns:
        A SummaryResponse with a concise summary of the moderation activity.
    """
    client = get_anthropic_client()
    
    # Format the decisions into a single string for the prompt
    decision_log = "\n".join(
        [f"- Text: '{d.text[:50]}...' | Decision: {d.decision} | Categories: {', '.join(d.categories)} | Time: {d.timestamp}" for d in request.decisions]
    )
    
    prompt = f"""
Here is a log of recent content moderation decisions. Please provide a brief, high-level summary.
Focus on identifying any trends, such as repeated violations by a user, or a spike in a particular category of violation.

Moderation Log:
{decision_log}

Summary:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    summary_text = message.content[0].text if message.content else "Could not generate summary."
    
    return SummaryResponse(summary_text=summary_text)
