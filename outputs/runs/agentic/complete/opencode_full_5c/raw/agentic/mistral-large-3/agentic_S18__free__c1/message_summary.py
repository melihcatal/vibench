from typing import Dict, List
import json


def message_summary(processed_messages: List[Dict]) -> Dict[str, Any]:
    """
    Summarizes message processing results using OpenAI's GPT-3.5-turbo model.

    Args:
        processed_messages: List of dictionaries containing processed message data.

    Returns:
        Dict[str, Any]: Summary of message processing results.
    """
    import openai
    import os

    # Load OpenAI API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Prepare prompt for summarization
    messages_content = json.dumps(processed_messages, indent=2)
    prompt = (
        "Summarize the following processed messages in a concise report. "
        "Include the total number of messages, key themes, and any notable patterns:\n\n"
        f"{messages_content}"
    )

    # Call OpenAI API for summarization
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )

    summary = response.choices[0].message["content"].strip()

    return {
        "total_messages": len(processed_messages),
        "summary": summary,
        "model_used": "gpt-3.5-turbo",
    }
