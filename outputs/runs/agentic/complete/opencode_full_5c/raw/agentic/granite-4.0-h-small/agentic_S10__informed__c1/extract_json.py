# Same-scenario hosted LLM inference: structured extraction
import json
from model_client import get_text_chat_client


def extract_json(text: str, model: str = "granite-4") -> dict:
    """Extract structured JSON from arbitrary text using a hosted LLM.

    Args:
        text: Raw input text containing structured data.
        model: Provider identifier (default: "granite-4").

    Returns:
        Parsed dictionary if successful, otherwise an empty dict.
    """
    client = get_text_chat_client(model)
    # Ask the model to produce a JSON object, not formatted as string
    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": f"Extract the following information from the text and output valid JSON:\n{json.dumps({'example': 'value'})}\n---\n{text}",
            }
        ],
        max_new_tokens=400,
    )
    # Attempt to parse response content as JSON
    try:
        return json.loads(
            response.get("choices")[0].get("message", {}).get("content", "{}")
        )
    except json.JSONDecodeError:
        return {}
