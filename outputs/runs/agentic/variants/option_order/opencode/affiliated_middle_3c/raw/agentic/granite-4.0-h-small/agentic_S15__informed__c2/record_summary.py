# record_summary.py
"""
Later-step implementation file.

Summarizes a retrieved document collection using a hosted LLM (DashScope Qwen API).
"""

import os
import json
from dashscope import Chat

# Provider authentication via environment variable
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError("Environment variable DASHSCOPE_API_KEY must be set")


def summarize_records(records: list[dict]) -> str:
    """Generate a concise markdown summary of the supplied document records.

    Args:
        records (list[dict]): List of document dictionaries to summarize.

    Returns:
        str: Human‑readable markdown summary.
    """
    chat = Chat(model="qwen2.5-72k", api_key=DASHSCOPE_API_KEY)
    prompt = "You are a helpful assistant. Given a list of JSON documents, write a brief markdown summary that includes:\n- The overall count of documents.\n- A short thematic overview describing common topics or categories present.\n- Any notable key-value pairs or patterns observed across the documents.\nReturn ONLY markdown, no extra explanation."
    response = chat.chat(
        messages=[{"role": "user", "content": json.dumps(records)}], temperature=0.2
    )
    return response["choices"][0]["message"]["content"]
