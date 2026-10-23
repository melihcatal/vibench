import os
from typing import List, Dict, Any
from openai import OpenAI

def summarize_processing_results(results: List[Dict[str, Any]]) -> str:
    """
    Summarizes message processing results using OpenAI's GPT model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    if not results:
        return "No messages were processed."

    prompt_content = "Summarize the following message processing results in one paragraph:\n\n"
    for result in results:
        prompt_content += f"- Message ID {result.get('message_id', 'N/A')}: Status {result.get('status', 'Unknown')}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes operational data."},
                {"role": "user", "content": prompt_content}
            ]
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        raise
