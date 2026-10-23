from openai import OpenAI
import os
from typing import Dict, Any


class MessageSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize(self, message_data: Dict[str, Any]) -> str:
        """
        Summarizes message processing results using OpenAI's GPT model.
        """
        prompt = f"Summarize the following message processing result in one sentence:\n{message_data}"
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()


def summarize_message(message_data: Dict[str, Any]) -> str:
    """
    Summarizes message processing results.
    """
    summarizer = MessageSummarizer()
    return summarizer.summarize(message_data)


if __name__ == "__main__":
    message_data = {
        "event_type": "user_action",
        "user_id": "12345",
        "action": "purchase",
        "status": "completed",
    }
    summary = summarize_message(message_data)
    print(f"Message summary: {summary}")
