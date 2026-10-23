import os
from typing import Any, Dict, List

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    client = _client()
    messages = [
        {
            "role": "system",
            "content": "Summarize incident findings from logs concisely.",
        },
        {"role": "user", "content": str(error_logs)},
    ]
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages)
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    incident_summary([])
