# LATER-STEP
# record_summary.py - Summarize retrieved document records

# Provider: Qwen via DashScope (hosted LLM inference)
import dashscope
from typing import List, Dict

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def summarize_records(records: List[Dict]) -> str:
    """Generate a concise summary of a list of document records using Qwen.

    The prompt instructs the model to produce a brief overview.

    Args:
        records (List[Dict]): List of document dictionaries to summarize.

    Returns:
        str: Human-readable summary text.
    """
    prompt = (
        "You are a helpful assistant. Given the following JSON document records, "
        "produce a short 2-3 sentence summary that captures the overall content."
    )
    prompt += "\n\n" + json.dumps(records, indent=2)
    response = dashscope.chatgpt.complete(
        system="You are a concise summarizer.",
        messages=[{"role": "user", "content": prompt}],
        model="qwen",
    )
    return response.choices[0].message.content
