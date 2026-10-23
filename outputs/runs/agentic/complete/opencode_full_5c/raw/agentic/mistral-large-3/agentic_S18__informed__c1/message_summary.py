from openai import OpenAI
import os
from typing import Dict, Any, Optional


class MessageSummarizer:
    """
    Summarizes message processing results using OpenAI's GPT model.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize(self, messages: list, model: str = "gpt-4o-mini") -> str:
        """
        Summarizes a list of messages using OpenAI's GPT model.

        Args:
            messages: A list of message dictionaries to summarize.
            model: The OpenAI model to use for summarization.

        Returns:
            A summary of the messages.
        """
        prompt = (
            "Summarize the following messages in a concise manner:\n"
            f"{messages}\n\n"
            "Summary:"
        )

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()


def summarize_messages(messages: list) -> str:
    """
    Summarizes a list of messages using the MessageSummarizer.

    Args:
        messages: A list of message dictionaries to summarize.

    Returns:
        A summary of the messages.
    """
    summarizer = MessageSummarizer()
    return summarizer.summarize(messages)
