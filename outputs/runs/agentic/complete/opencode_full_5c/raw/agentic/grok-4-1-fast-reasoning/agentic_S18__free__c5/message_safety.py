import os
import sys
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    if not input_data:
        print(json.dumps({"safety": {"safe": True, "reason": "No input"}}))
        sys.exit(0)
    msg_data = json.loads(input_data)
    data_str = msg_data.get("data", "{}")
    try:
        payload = json.loads(data_str)
    except json.JSONDecodeError:
        payload = {}
    content = payload.get("content", "")
    if not content:
        output = msg_data.copy()
        output["safety"] = {"safe": True, "reason": "No content"}
        print(json.dumps(output))
        sys.exit(0)
    moderation = client.moderations.create(
        input=content, model="text-moderation-latest"
    )
    result = moderation.results[0]
    safe = not result.flagged
    output = msg_data.copy()
    output["safety"] = {
        "safe": safe,
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
    print(json.dumps(output))
