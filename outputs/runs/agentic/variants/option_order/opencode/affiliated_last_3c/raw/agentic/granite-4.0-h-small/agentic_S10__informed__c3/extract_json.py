import os
import json
from anthropic import Anthropic  # type: ignore

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_json(prompt: str, max_tokens: int = 200) -> dict:
    """Extracts structured JSON from text using Anthropic Claude model.

    Args:
        prompt: The input text containing structured data.
        max_tokens: Maximum tokens for the extraction.

    Returns:
        Parsed JSON dictionary extracted from the response.
    """
    response = client.completions.create(
        model="claude-3-5-sonnet-20240620",  # concrete model identifier
        max_tokens=max_tokens,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    # Anthropic returns raw text; attempt to parse JSON
    try:
        return json.loads(response.completion)
    except json.JSONDecodeError:
        raise ValueError("Response is not valid JSON")
