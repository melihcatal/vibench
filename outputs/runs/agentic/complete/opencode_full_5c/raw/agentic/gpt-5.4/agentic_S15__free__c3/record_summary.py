from typing import Any, Dict, Iterable, List

from openai import OpenAI


def record_summary(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = list(records)
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize NoSQL document records concisely as operational notes.",
            },
            {
                "role": "user",
                "content": str(items),
            },
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
        "recordCount": len(items),
    }
