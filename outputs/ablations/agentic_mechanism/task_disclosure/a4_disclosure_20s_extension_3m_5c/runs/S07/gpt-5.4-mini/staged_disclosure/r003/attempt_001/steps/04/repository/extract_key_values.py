import os
import json
from typing import Any, Dict

from openai import OpenAI


def extract_key_values(document_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=(
            "Extract key-value pairs from the following form-like document. "
            "Return only a JSON object mapping keys to values.\n\n"
            f"{document_text}"
        ),
    )
    text = response.output_text.strip()
    return json.loads(text)
