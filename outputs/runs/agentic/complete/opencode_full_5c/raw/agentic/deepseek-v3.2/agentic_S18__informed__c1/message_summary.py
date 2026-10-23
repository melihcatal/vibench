import os
from anthropic import Anthropic


def summarize_message_processing(results):
    """Summarize message processing results using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = Anthropic(api_key=api_key)

    summary_prompt = f"""
    Summarize the following message processing results:
    
    Total messages: {results.get("total_messages", 0)}
    Successfully processed: {results.get("successful", 0)}
    Failed: {results.get("failed", 0)}
    Dead lettered: {results.get("dead_lettered", 0)}
    
    Processing time: {results.get("processing_time", "N/A")}
    Average processing time per message: {results.get("avg_processing_time", "N/A")}
    
    Errors encountered: {results.get("errors", [])}
    
    Provide a concise summary highlighting:
    1. Overall success rate
    2. Main issues if any
    3. Recommendations for improvement
    """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    summary = response.content[0].text

    return {
        "summary": summary,
        "model_used": "claude-3-haiku-20240307",
        "total_messages": results.get("total_messages", 0),
        "success_rate": (
            results.get("successful", 0) / max(results.get("total_messages", 1), 1)
        )
        * 100,
    }
