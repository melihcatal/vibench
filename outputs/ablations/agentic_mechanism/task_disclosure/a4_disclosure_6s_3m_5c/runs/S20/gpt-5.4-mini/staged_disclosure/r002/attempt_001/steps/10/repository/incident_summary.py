import os
from typing import Any, Dict, List

from openai import OpenAI


def summarize_incident(errors: List[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these error-log findings for an incident review:\n" + "\n".join(f"- {error}" for error in errors)
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"provider": "openai", "model": "gpt-5.4-mini", "summary": response.output_text}


if __name__ == "__main__":
    import json
    import sys

    errors = sys.argv[1:]
    result = summarize_incident(errors)
    print(json.dumps(result, ensure_ascii=False))
