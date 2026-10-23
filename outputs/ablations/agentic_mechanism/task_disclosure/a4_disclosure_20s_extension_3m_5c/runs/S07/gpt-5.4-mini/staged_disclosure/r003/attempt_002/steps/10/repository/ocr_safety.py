import os
from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def check_extracted_document_text(text: str) -> Dict[str, Any]:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You review extracted document text for unsafe content. "
                    "Return only valid JSON with keys: unsafe (boolean), "
                    "categories (array of strings), rationale (string), "
                    "highlights (array of strings)."
                ),
            },
            {
                "role": "user",
                "content": f"Check this extracted document text:\n\n{text}",
            },
        ],
        temperature=0,
    )

    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_items: List[str] = []
        for item in getattr(response, "output", []):
            for content in getattr(item, "content", []):
                text_part = getattr(content, "text", None)
                if text_part:
                    output_items.append(text_part)
        output_text = "".join(output_items)

    import json

    return json.loads(output_text)
