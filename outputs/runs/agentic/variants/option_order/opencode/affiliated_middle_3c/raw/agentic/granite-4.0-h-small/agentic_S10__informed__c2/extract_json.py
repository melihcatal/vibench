# Extract structured JSON from text using DashScope Qwen API
import os
from dashscope import text
from model_client import get_dashscope_client


def extract_json(input_text: str, model: str = "qwen-plus") -> dict:
    """Extract structured JSON from text using DashScope Qwen model.

    Args:
        input_text (str): Prompt containing the text to extract JSON from.
        model (str): Qwen model identifier (default: "qwen-plus").

    Returns:
        dict: Parsed JSON object.
    """
    client = get_dashscope_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        temperature=0.0,
    )
    # Assume the model responds with a JSON string wrapped in backticks
    json_str = response.choices[0].message.content.strip()
    return json.loads(json_str)
