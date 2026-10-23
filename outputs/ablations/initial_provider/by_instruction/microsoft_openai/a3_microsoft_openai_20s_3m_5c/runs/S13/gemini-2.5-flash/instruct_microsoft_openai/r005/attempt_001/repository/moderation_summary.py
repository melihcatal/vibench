import os
from openai import OpenAI
from typing import Dict, Any, List

def moderation_summary(moderation_results: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using OpenAI's GPT models.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Construct a prompt for summarization
    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes moderation decisions."},
        {"role": "user", "content": f"Summarize the following moderation results:\n{moderation_results}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a common GPT model for summarization
            messages=prompt_messages,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing moderation results: {str(e)}"

if __name__ == "__main__":
    # Example Usage
    sample_moderation_results = [
        {"text": "I love this product!", "hate": 0, "self_harm": 0, "sexual": 0, "violence": 0, "decision": "allow"},
        {"text": "Kill all humans!", "hate": 5, "self_harm": 0, "sexual": 0, "violence": 5, "decision": "deny", "reasons": ["Category 'hate' with severity 5 exceeded threshold 3.", "Category 'violence' with severity 5 exceeded threshold 3."]},
        {"text": "I'm feeling down.", "hate": 0, "self_harm": 2, "sexual": 0, "violence": 0, "decision": "allow"}
    ]
    summary = moderation_summary(sample_moderation_results)
    print(f"Moderation Summary:\n{summary}")
