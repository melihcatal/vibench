from openai import OpenAI
import os
from typing import Dict, Any, List

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def message_summary(messages: List[Dict[str, Any]]) -> str:
    """
    Summarizes message processing results using OpenAI's GPT model.

    Args:
        messages: List of message dictionaries to summarize.

    Returns:
        str: A summary of the message processing results.
    """
    message_texts = [str(message) for message in messages]
    prompt = (
        "Summarize the following messages in a concise manner:\n\n"
        f"{'\\n'.join(message_texts)}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
